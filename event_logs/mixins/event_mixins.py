import sys

from django.contrib.auth.models import AnonymousUser
from event_logs.models import EventLog
from logger_egine import logger

VIEW_EVENTS = ['RETRIEVE', "LIST"]
DESIRED_EVENTS = ['CREATE', 'UPDATE', 'PARTIAL_UPDATE', 'DESTROY']
# VIEW_EVENTS = ["GET", "LIST"]
# DESIRED_EVENTS = ['POST', 'PUT', 'PATCH', 'DELETE']

MESSAGE_ACTIONS = {
    'CREATE': "Created",
    'UPDATE': "Updated",
    'PARTIAL_UPDATE': "Updated",
    'DELETE': "Deleted",
    "GET": "Viewed",
    "LIST": "Viewed"
}
EVENT_MODEL_ACTIONS = {
    'CREATE': "CREATE",
    'UPDATE': "UPDATE",
    'PARTIAL_UPDATE': "UPDATE",
    'DESTROY': "DELETE",
    'RETRIEVE': "GET",
    "LIST": "LIST"
}
FAIL = "Fail"
SUCCESS = "Success"


class EventLogsMixin:
    log_index = "EventMixin"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log_dict = dict(
            user=None, action='', url_path=None, model_name="", status="PENDING", message="", object_id=None
        )
        self.can_log = False
        self.event_log_instance = None

    def initial(self, request, *args, **kwargs):
        logger.debug(self.log_index, "Processing the Initials for the request")
        current_action = self.action.upper() if self.action else ""
        if current_action not in VIEW_EVENTS and current_action in DESIRED_EVENTS:
            self.can_log = True
        else:
            self.can_log = False

        if self.can_log:
            if current_action:
                logger.debug(index=self.log_index, message="Current action: %s" % current_action)
                current_query_set = getattr(self, "queryset", None)
                current_model_name = current_query_set.model.__name__ if current_query_set else 'UnknownModel'
                current_user = request.user if not isinstance(request.user, AnonymousUser) else None
                logger.debug(index=self.log_index, message="User %s has performed %s action on %s" % (
                    current_user, current_action, current_model_name))
                self.log_dict['user'] = current_user
                self.log_dict['action'] = current_action
                self.log_dict['model_name'] = current_model_name
                self.log_dict['url_path'] = request.path
                self.create_or_update_event()
            else:
                logger.critical(self.log_index, message="Invalid action was provided: %s" % current_action)
        return super().initial(request, *args, **kwargs)

    def handle_exception(self, exc):
        logger.debug(self.log_index, f"Handling the Exception, Exception: {exc}")
        if self.can_log:
            self.log_dict['status'] = "Fail"
            self.create_or_update_event()
        return super().handle_exception(exc)

    def initialize_request(self, request, *args, **kwargs):
        logger.debug(self.log_index, "Initializing the request")
        return super().initialize_request(request, *args, **kwargs)

    def finalize_response(self, request, response, *args, **kwargs):
        if self.can_log:
            logger.debug(self.log_index, "Finalizing the Response")
            self.log_dict['status'] = SUCCESS if 200 <= response.status_code < 300 else FAIL
            logger.debug(self.log_index, "Request completed: %s" % self.log_dict['message'])
            self.create_or_update_event()
        return super().finalize_response(request, response, *args, **kwargs)

    def format_message(self):
        action = MESSAGE_ACTIONS[self.log_dict['action']] if self.log_dict['action'] in MESSAGE_ACTIONS else \
            self.log_dict['action']
        user_name = self.log_dict['user'].username if self.log_dict['user'] is not None else None
        if self.log_dict['status'] == SUCCESS:
            return "%s has %s %s" % (user_name.title(), action, self.log_dict['model_name'])
        else:
            return "%s has failed to %s the %s" % (
                user_name.title(), self.log_dict['action'], self.log_dict['model_name'])

    def create_or_update_event(self):
        action = EVENT_MODEL_ACTIONS[self.log_dict['action']] if self.log_dict[
                                                                     'action'] in EVENT_MODEL_ACTIONS else "PENDING"
        if self.event_log_instance is None:
            self.event_log_instance = EventLog.objects.create(
                user=self.log_dict['user'],
                action=action,
                model_name=self.log_dict['model_name'],
                status=self.log_dict['status'],
                message=self.format_message(),
                object_id=self.log_dict['object_id'],
                url_path=self.log_dict['url_path'],
            )
        else:
            logger.debug(self.log_index, "Current Log entry: %d" % self.event_log_instance.id)
            EventLog.objects.filter(id=self.event_log_instance.id).update(
                user=self.log_dict['user'],
                action=action,
                model_name=self.log_dict['model_name'],
                status=self.log_dict['status'],
                message=self.format_message(),
                object_id=self.log_dict['object_id'],
                url_path=self.log_dict['url_path'],
            )
        # self.event_log_instance.save()
