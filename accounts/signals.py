from django.db.models.signals import pre_save, post_save
from accounts.models import User
from logger_egine import logger


def pre_user_process(sender, instance,  **kwargs):
    log_index = "Pre User Process"
    try:
        logger.debug(log_index, f"Received a request from the sender: {sender} | Args: {kwargs}")
        logger.debug(log_index, f"Processing: {instance.id}")

    except:
        pass


def post_user_process(sender, instance, created, **kwargs):
    log_index = "Post User Process"

    try:
        logger.debug(log_index, f"Received a request from the sender: {sender} | Args: {kwargs}")
        logger.debug(log_index, f"Processing: {instance.id}")

        if created:
            logger.debug(log_index, f"Newly created instance: {instance.id}")
        else:
            logger.debug(log_index, f"Existing instance: {instance.id}")


    except:
        pass


pre_save.connect(pre_user_process, User)
post_save.connect(post_user_process, User)
