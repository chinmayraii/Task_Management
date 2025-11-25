from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'created_date', 'due_date']
        read_only_fields = ['id', 'created_date']

    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value.strip()

    def validate_status(self, value):
        valid_statuses = [choice[0] for choice in Task.STATUS_CHOICES]
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value

    def validate_priority(self, value):
        valid_priorities = [choice[0] for choice in Task.PRIORITY_CHOICES]
        if value not in valid_priorities:
            raise serializers.ValidationError(f"Priority must be one of: {', '.join(valid_priorities)}")
        return value

