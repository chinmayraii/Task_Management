from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all()
        status_filter = self.request.query_params.get('status', None)
        priority_filter = self.request.query_params.get('priority', None)
        search = self.request.query_params.get('search', None)

        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if priority_filter:
            queryset = queryset.filter(priority=priority_filter)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        return queryset

    @action(detail=True, methods=['post'])
    def mark_complete(self, request, pk=None):
        task = self.get_object()
        task.status = 'complete'
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_incomplete(self, request, pk=None):
        task = self.get_object()
        task.status = 'incomplete'
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)
