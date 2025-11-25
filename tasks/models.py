from django.db import models
from django.core.validators import MinLengthValidator
from django.utils import timezone


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    STATUS_CHOICES = [
        ('incomplete', 'Incomplete'),
        ('complete', 'Complete'),
    ]

    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(1)],
        help_text='Task title'
    )
    description = models.TextField(blank=True, help_text='Task description')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='incomplete',
        help_text='Task status'
    )
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='medium',
        help_text='Task priority'
    )
    created_date = models.DateTimeField(auto_now_add=True, help_text='Task creation date')
    due_date = models.DateTimeField(null=True, blank=True, help_text='Task due date')

    class Meta:
        ordering = ['-created_date']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return self.title

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.due_date and self.due_date < timezone.now():
            raise ValidationError("Due date cannot be in the past.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
