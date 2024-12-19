from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import EventLog, UserLoginEvents
from .serializers import EventLogSerializer, UserLoginEventSerializer


class EventLogViewSet(viewsets.ViewSet):
    """A ViewSet for listing the Events"""

    def list(self, request):
        queryset = EventLog.objects.all()
        serializer = EventLogSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserLoginEventViewSet(viewsets.ViewSet):
    """A ViewSet for listing the Events"""

    def list(self, request):
        queryset = UserLoginEvents.objects.all().order_by('-id')
        serializer = UserLoginEventSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
