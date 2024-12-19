from django.urls import path

from rest_framework.routers import DefaultRouter

from logger_egine import logger

from .views import home, UserViewSet

logger.debug(index="UrlsInitialization", message="Initializing the account urls")

urlpatterns = [
    path('home/', home),
]

logger.debug(index="RoutesInitialization", message="Initializing the account routes")

router = DefaultRouter(trailing_slash=False)
router.register("user", UserViewSet)

urlpatterns += router.urls

logger.debug(index="RoutesInitialization", message="Initializing the account routes is successful")

logger.debug(index="UrlsInitialization", message="Initializing the account urls is successful")
