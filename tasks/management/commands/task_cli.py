from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from datetime import datetime
from tasks.models import Task


class Command(BaseCommand):
    help = 'Task Management CLI - Create, read, update, and delete tasks'

    def add_arguments(self, parser):
        parser.add_argument(
            'action',
            type=str,
            choices=['create', 'list', 'get', 'update', 'delete', 'complete', 'incomplete'],
            help='Action to perform'
        )
        parser.add_argument('--id', type=int, help='Task ID (for get, update, delete, complete, incomplete)')
        parser.add_argument('--title', type=str, help='Task title')
        parser.add_argument('--description', type=str, help='Task description', default='')
        parser.add_argument('--priority', type=str, choices=['low', 'medium', 'high'], default='medium', help='Task priority')
        parser.add_argument('--status', type=str, choices=['incomplete', 'complete'], default='incomplete', help='Task status')
        parser.add_argument('--due-date', type=str, help='Due date (YYYY-MM-DD or YYYY-MM-DD HH:MM)')
        parser.add_argument('--filter-status', type=str, choices=['incomplete', 'complete'], help='Filter tasks by status')
        parser.add_argument('--filter-priority', type=str, choices=['low', 'medium', 'high'], help='Filter tasks by priority')
        parser.add_argument('--search', type=str, help='Search tasks by title or description')

    def handle(self, *args, **options):
        action = options['action']

        try:
            if action == 'create':
                self.create_task(options)
            elif action == 'list':
                self.list_tasks(options)
            elif action == 'get':
                self.get_task(options)
            elif action == 'update':
                self.update_task(options)
            elif action == 'delete':
                self.delete_task(options)
            elif action == 'complete':
                self.mark_complete(options)
            elif action == 'incomplete':
                self.mark_incomplete(options)
        except Exception as e:
            raise CommandError(f'Error: {str(e)}')

    def create_task(self, options):
        if not options['title']:
            raise CommandError('Title is required for creating a task. Use --title')

        due_date = None
        if options['due_date']:
            try:
                if ' ' in options['due_date']:
                    due_date = datetime.strptime(options['due_date'], '%Y-%m-%d %H:%M')
                else:
                    due_date = datetime.strptime(options['due_date'], '%Y-%m-%d')
                due_date = timezone.make_aware(due_date)
            except ValueError:
                raise CommandError('Invalid date format. Use YYYY-MM-DD or YYYY-MM-DD HH:MM')

        task = Task.objects.create(
            title=options['title'],
            description=options['description'],
            priority=options['priority'],
            status=options['status'],
            due_date=due_date
        )

        self.stdout.write(self.style.SUCCESS(f'Task created successfully!'))
        self.display_task(task)

    def list_tasks(self, options):
        tasks = Task.objects.all()

        if options['filter_status']:
            tasks = tasks.filter(status=options['filter_status'])
        if options['filter_priority']:
            tasks = tasks.filter(priority=options['filter_priority'])
        if options['search']:
            tasks = tasks.filter(
                title__icontains=options['search']
            ) | tasks.filter(
                description__icontains=options['search']
            )

        if not tasks.exists():
            self.stdout.write(self.style.WARNING('No tasks found.'))
            return

        self.stdout.write(self.style.SUCCESS(f'\nFound {tasks.count()} task(s):\n'))
        for task in tasks:
            self.display_task(task)
            self.stdout.write('-' * 80)

    def get_task(self, options):
        if not options['id']:
            raise CommandError('Task ID is required. Use --id')

        try:
            task = Task.objects.get(pk=options['id'])
            self.display_task(task)
        except Task.DoesNotExist:
            raise CommandError(f'Task with ID {options["id"]} does not exist.')

    def update_task(self, options):
        if not options['id']:
            raise CommandError('Task ID is required. Use --id')

        try:
            task = Task.objects.get(pk=options['id'])
        except Task.DoesNotExist:
            raise CommandError(f'Task with ID {options["id"]} does not exist.')

        if options['title']:
            task.title = options['title']
        if options['description'] is not None:
            task.description = options['description']
        if options['priority']:
            task.priority = options['priority']
        if options['status']:
            task.status = options['status']
        if options['due_date']:
            try:
                if ' ' in options['due_date']:
                    due_date = datetime.strptime(options['due_date'], '%Y-%m-%d %H:%M')
                else:
                    due_date = datetime.strptime(options['due_date'], '%Y-%m-%d')
                task.due_date = timezone.make_aware(due_date)
            except ValueError:
                raise CommandError('Invalid date format. Use YYYY-MM-DD or YYYY-MM-DD HH:MM')

        task.save()
        self.stdout.write(self.style.SUCCESS('Task updated successfully!'))
        self.display_task(task)

    def delete_task(self, options):
        if not options['id']:
            raise CommandError('Task ID is required. Use --id')

        try:
            task = Task.objects.get(pk=options['id'])
            task_title = task.title
            task.delete()
            self.stdout.write(self.style.SUCCESS(f'Task "{task_title}" deleted successfully!'))
        except Task.DoesNotExist:
            raise CommandError(f'Task with ID {options["id"]} does not exist.')

    def mark_complete(self, options):
        if not options['id']:
            raise CommandError('Task ID is required. Use --id')

        try:
            task = Task.objects.get(pk=options['id'])
            task.status = 'complete'
            task.save()
            self.stdout.write(self.style.SUCCESS('Task marked as complete!'))
            self.display_task(task)
        except Task.DoesNotExist:
            raise CommandError(f'Task with ID {options["id"]} does not exist.')

    def mark_incomplete(self, options):
        if not options['id']:
            raise CommandError('Task ID is required. Use --id')

        try:
            task = Task.objects.get(pk=options['id'])
            task.status = 'incomplete'
            task.save()
            self.stdout.write(self.style.SUCCESS('Task marked as incomplete!'))
            self.display_task(task)
        except Task.DoesNotExist:
            raise CommandError(f'Task with ID {options["id"]} does not exist.')

    def display_task(self, task):
        self.stdout.write(f'\nID: {task.id}')
        self.stdout.write(f'Title: {task.title}')
        self.stdout.write(f'Description: {task.description or "(No description)"}')
        self.stdout.write(f'Status: {task.status.upper()}')
        self.stdout.write(f'Priority: {task.priority.upper()}')
        self.stdout.write(f'Created: {task.created_date.strftime("%Y-%m-%d %H:%M:%S")}')
        if task.due_date:
            self.stdout.write(f'Due Date: {task.due_date.strftime("%Y-%m-%d %H:%M:%S")}')
        else:
            self.stdout.write('Due Date: (No due date)')

