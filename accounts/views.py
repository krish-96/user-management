import json
from typing import Optional, Dict

from django.http import HttpResponse, HttpRequest, HttpHeaders

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token

from logger_egine import logger

from .models import User
from .serilaizers import UserSerializer, PasswordSerializer, UserLoginSerializer

from .utils.user import get_client_ip, get_client_loc_details

from event_logs.mixins import EventLogsMixin
from event_logs.models import UserLoginEvents

from django.contrib.auth.signals import user_logged_in, user_login_failed


# Create your views here.


def home(request):
    logger.info("HomePage", "Home Page Accessed %s" % request.user)
    return HttpResponse("Home Page")


class UserViewSet(EventLogsMixin, viewsets.ModelViewSet):
    """
    This ViewSet is created to work with the User model.
    Any info related to user should present here.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    log_index = "UserViewSet"

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        ip_address = get_client_ip(self.request)
        print(f"ip_address: {ip_address}")
        get_client_loc_details(ip_address)
        return User.objects.all()

    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the action.
        """
        if self.action == 'login':
            return UserLoginSerializer
        elif self.action == 'change_password':
            return PasswordSerializer

        return super().get_serializer_class()

    def update_user_login_status(self, user: Optional[User] = None, status=False,
                                 reason: str = "", data: Dict = None,
                                 request: Optional[HttpRequest] = None):
        """
        This method will update the user's login status into the database
        :param user: The user object, if successful login
        :param status: The status of login attempt (True/False)
        :param reason: reason i.e., Logging successful or failed (str)
        :param data: Given user data
        :param request: the actual request to fetch more info about the user like ip address
        return: None
        """
        try:
            logger.debug(self.log_index, message="Updating the user login status")
            data = {} if not data else data
            if request:
                ip = get_client_ip(request)
                data['ip'] = ip
                data['request_method'] = request.method

                data['headers'] = {
                    "Content-Length": request.headers.get("Content-Length", None),
                    "Content-Type": request.headers.get("Content-Type", None),
                    "Sec-Ch-Ua-Platform": request.headers.get("Sec-Ch-Ua-Platform", None),
                    "Accept": request.headers.get("Accept", None),
                    "Sec-Ch-Ua": request.headers.get("Sec-Ch-Ua", None),
                    "Accept-Language": request.headers.get("Accept-Language", None),
                }

                data['user_agent'] = request.headers["User-Agent"] if "User-Agent" in request.headers else ""
                data["additional_data"] = {}
                if data['user_agent']:
                    from user_agents import parse
                    parsed_user_agent = parse(data['user_agent'])
                    print(f"parsed_user_agent: {parsed_user_agent}")

                    data['additional_data'] = dict(
                        os=parsed_user_agent.get_os(),
                        device=parsed_user_agent.get_device(),
                        browser=parsed_user_agent.get_browser()
                    )

                data['geo_location'] = get_client_loc_details(ip)

            print(f"Received data for the failed login is: {data}")
            user_login_event_obj = UserLoginEvents(is_success=status, reason=reason, user_data=data)
            if user is not None:
                user_login_event_obj.user = user

            user_login_event_obj.save()
            logger.debug(self.log_index, message="Updating the user login status is successful")
        except Exception as err:
            logger.error(self.log_index, message=f"Failed to update the user login status, Exception: {err}")

    @action(detail=False, methods=["POST"], permission_classes=[AllowAny])
    def login(self, request):
        if request.method == "POST":
            logger.info(self.log_index, "Login data received...")
            password = request.data.get('password')
            username = request.data.get('username')
            logger.info(self.log_index, f"Login data received...: {username} | {password}")
            if not (username and password):
                return Response({"error": "Username and Password are required!"}, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.filter(username=username).first()
            if not user:
                self.update_user_login_status(
                    reason="User Not Found",
                    data=dict(username=username),
                    request=request
                )
                return Response({"error": "User Not Found!"}, status=status.HTTP_400_BAD_REQUEST)
            user_data = dict()
            if user.check_password(password):
                user_data['username'] = user.username
                user_data['email'] = user.email
                token, _ = Token.objects.get_or_create(user=user)
                user_data['token'] = str(token.key)
                logger.info(self.log_index, "User authenticated successfully.")

                self.update_user_login_status(
                    status=True,
                    reason=f"{user.username} Logged in successfully",
                    user=user
                )
                return Response(user_data, status=status.HTTP_200_OK)
            else:
                logger.error(self.log_index, "Login failed: Invalid password")
                self.update_user_login_status(
                    status=True,
                    reason="Invalid password",
                    user=user,
                    data=dict(username=username),
                    request=request
                )
                return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)

        logger.debug(self.log_index, "Login page accessed")
        serializer = self.get_serializer()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated],
            authentication_classes=[BasicAuthentication, TokenAuthentication])
    def change_password(self, request, pk=None):
        if request.method == 'POST':
            serializer = self.get_serializer(request.data)
            print(f"Requested user: {request.user.username}")
            password = request.data.get('password')
            confirm_password = request.data.get('confirm_password')
            if password != confirm_password:
                return Response({"error": "Password and Confirm Password must be same!"}, status=status.HTTP_200_OK)
            if not request.user.is_anonymous and password == confirm_password:
                user = request.user
                user.set_password(password)
                user.save()
                return Response(dict(message="Password changed successfully."), status=status.HTTP_200_OK)

            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer()
        return Response(serializer.data, status=status.HTTP_200_OK)
