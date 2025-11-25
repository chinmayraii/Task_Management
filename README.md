# Task Management API with CLI Interface

A RESTful Task Management system built with Django and Django REST Framework, featuring both an API backend and a command-line interface.

## Features

- **RESTful API**: Full CRUD operations for task management
- **CLI Interface**: Command-line tool for interacting with tasks
- **Data Persistence**: SQLite database for data storage
- **Filtering & Search**: Filter tasks by status, priority, and search by title/description
- **Validation**: Comprehensive data validation for task fields
- **Priority Levels**: Support for low, medium, and high priority tasks
- **Status Management**: Mark tasks as complete or incomplete

## Requirements

- Python 3.8+
- Django 4.2+
- Django REST Framework 3.14+

## Setup Instructions

1. **Clone or navigate to the project directory:**
   ```bash
   cd Task_Management
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (optional, for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/api/`

## API Endpoint Documentation

### Base URL
```
http://127.0.0.1:8000/api/tasks/
```

### Endpoints

#### List Tasks
- **GET** `/api/tasks/`
- **Description**: Retrieve a list of all tasks
- **Query Parameters**:
  - `status` (optional): Filter by status (`incomplete` or `complete`)
  - `priority` (optional): Filter by priority (`low`, `medium`, or `high`)
  - `search` (optional): Search in title or description
- **Example**: `GET /api/tasks/?status=incomplete&priority=high&search=meeting`

#### Get Task
- **GET** `/api/tasks/{id}/`
- **Description**: Retrieve a specific task by ID
- **Example**: `GET /api/tasks/1/`

#### Create Task
- **POST** `/api/tasks/`
- **Description**: Create a new task
- **Request Body**:
  ```json
  {
    "title": "Task title",
    "description": "Task description",
    "status": "incomplete",
    "priority": "medium",
    "due_date": "2024-12-31T23:59:59Z"
  }
  ```
- **Note**: `status` defaults to `incomplete`, `priority` defaults to `medium`, `due_date` is optional

#### Update Task
- **PUT** `/api/tasks/{id}/` (full update)
- **PATCH** `/api/tasks/{id}/` (partial update)
- **Description**: Update an existing task
- **Request Body**: Same as Create Task (all fields optional for PATCH)

#### Delete Task
- **DELETE** `/api/tasks/{id}/`
- **Description**: Delete a task by ID

#### Mark Task as Complete
- **POST** `/api/tasks/{id}/mark_complete/`
- **Description**: Mark a task as complete

#### Mark Task as Incomplete
- **POST** `/api/tasks/{id}/mark_incomplete/`
- **Description**: Mark a task as incomplete

### Task Model Fields

- `id`: Auto-generated unique identifier (read-only)
- `title`: Task title (required, max 200 characters)
- `description`: Task description (optional)
- `status`: Task status - `incomplete` or `complete` (default: `incomplete`)
- `priority`: Task priority - `low`, `medium`, or `high` (default: `medium`)
- `created_date`: Auto-generated creation timestamp (read-only)
- `due_date`: Optional due date (ISO 8601 format)

## CLI Usage Examples

The CLI tool is accessible via Django's management command system.

### Create a Task
```bash
python manage.py task_cli create --title "Complete project" --description "Finish the task management project" --priority high --due-date "2024-12-31"
```

### List All Tasks
```bash
python manage.py task_cli list
```

### List Tasks with Filters
```bash
python manage.py task_cli list --filter-status incomplete --filter-priority high
python manage.py task_cli list --search "meeting"
```

### Get a Specific Task
```bash
python manage.py task_cli get --id 1
```

### Update a Task
```bash
python manage.py task_cli update --id 1 --title "Updated title" --priority low --status complete
```

### Delete a Task
```bash
python manage.py task_cli delete --id 1
```

### Mark Task as Complete
```bash
python manage.py task_cli complete --id 1
```

### Mark Task as Incomplete
```bash
python manage.py task_cli incomplete --id 1
```

### CLI Command Reference

**Actions:**
- `create`: Create a new task
- `list`: List tasks (with optional filters)
- `get`: Get a specific task by ID
- `update`: Update a task
- `delete`: Delete a task
- `complete`: Mark a task as complete
- `incomplete`: Mark a task as incomplete

**Options:**
- `--id`: Task ID (required for get, update, delete, complete, incomplete)
- `--title`: Task title (required for create)
- `--description`: Task description
- `--priority`: Task priority (`low`, `medium`, `high`)
- `--status`: Task status (`incomplete`, `complete`)
- `--due-date`: Due date (format: `YYYY-MM-DD` or `YYYY-MM-DD HH:MM`)
- `--filter-status`: Filter tasks by status
- `--filter-priority`: Filter tasks by priority
- `--search`: Search tasks by title or description

## Assumptions

1. **Database**: SQLite is used for simplicity and portability. For production, consider PostgreSQL or MySQL.
2. **Authentication**: The API does not include authentication/authorization. For production, implement proper authentication (e.g., token-based authentication).
3. **Date Format**: Due dates accept ISO 8601 format in API and `YYYY-MM-DD` or `YYYY-MM-DD HH:MM` in CLI.
4. **Validation**: Due dates cannot be in the past (enforced in model validation).
5. **Default Values**: New tasks default to `incomplete` status and `medium` priority.

## Project Structure

```
Task_Management/
├── manage.py
├── requirements.txt
├── README.md
├── taskmanager/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── tasks/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── serializers.py
    ├── urls.py
    ├── views.py
    ├── tests.py
    └── management/
        └── commands/
            ├── __init__.py
            └── task_cli.py
```

## Testing the API

You can test the API using curl, Postman, or any HTTP client:

**Create a task:**
```bash
curl -X POST http://127.0.0.1:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Task", "description": "This is a test", "priority": "high"}'
```

**List tasks:**
```bash
curl http://127.0.0.1:8000/api/tasks/
```

**Update a task:**
```bash
curl -X PATCH http://127.0.0.1:8000/api/tasks/1/ \
  -H "Content-Type: application/json" \
  -d '{"status": "complete"}'
```

## Admin Interface

Access the Django admin interface at `http://127.0.0.1:8000/admin/` after creating a superuser. The admin interface provides a web-based UI for managing tasks.

## Error Handling

The API returns appropriate HTTP status codes:
- `200 OK`: Successful GET, PUT, PATCH requests
- `201 Created`: Successful POST request
- `204 No Content`: Successful DELETE request
- `400 Bad Request`: Validation errors
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server errors

Validation errors are returned in JSON format with detailed error messages.
