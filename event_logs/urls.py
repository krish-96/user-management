from django.urls import path, include

from logger_egine import logger

from .views import EventLogViewSet, UserLoginEventViewSet

logger.debug("UrlsInitialization", "Initializing the Event Logs App urls")

urlpatterns = [
    # path('', EventLogViewSet.as_view()),

]

logger.debug("UrlsInitialization", "Initializing the Event Logs App urls is successful")

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('events', EventLogViewSet, basename="events")
router.register('user-login/events', UserLoginEventViewSet, basename="user-login-events")
urlpatterns += router.urls
