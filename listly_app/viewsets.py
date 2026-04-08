from rest_framework import viewsets

from listly_app.models import task
from listly_app.serializer import UserTaskSerializer

class tasksViewSet(viewsets.ModelViewSet):
    """ViewSet for the task model"""

    queryset = task.objects.all()
    serializer_class = UserTaskSerializer
    lookup_field = "pk"