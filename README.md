# Django CRM System

Django CRM System is a web application for managing clients, tasks, deals, and task comments.

The main focus of this project is backend development with Django: models, relationships, CRUD operations, authentication, role-based permissions, search, filtering, tests, code quality, and database query optimization.

---

## Features

- Custom user model with roles
- Authentication
- Role-based permissions
- Client, task, and deal management
- Task comments with edit/delete functionality
- Search and filtering
- Pagination
- Minimal Bootstrap-based UI
- Light/Dark theme switcher
- Query optimization with `select_related` and `prefetch_related`
- Tests for core backend logic
- Flake8 code quality checks

---

## User Roles

### Admin

- Can view all clients, tasks, and deals
- Can delete clients, tasks, and deals
- Can edit and delete any task comment

### Manager

- Can view only their own clients
- Can view tasks created by them or assigned to them
- Can view only their own deals
- Can create clients, tasks, deals, and comments
- Can edit and delete only their own comments

### Support

- Can view only tasks assigned to them
- Can create task comments
- Can edit and delete only their own comments

---

## Main Models

- **User** — custom user model with phone, position, and role
- **Client** — customer information
- **Task** — work item related to a client
- **TaskComment** — comments inside tasks
- **Deal** — sales/opportunity entity related to a client

---

## Tech Stack

- Python
- Django
- SQLite
- HTML
- CSS
- Bootstrap 5
- Bootstrap Icons
- Django TestCase
- Flake8

---

## Project Structure

```text
django-crm-system/
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── crm/
│   ├── forms/
│   │   ├── client_forms.py
│   │   ├── deal_forms.py
│   │   ├── task_comment_forms.py
│   │   └── task_forms.py
│   │
│   ├── static/
│   │   └── crm/
│   │       └── css/
│   │           └── styles.css
│   │
│   ├── templates/
│   │   ├── crm/
│   │   │   ├── clients/
│   │   │   ├── deals/
│   │   │   ├── includes/
│   │   │   ├── tasks/
│   │   │   ├── base.html
│   │   │   └── dashboard.html
│   │   │
│   │   └── registration/
│   │       └── login.html
│   │
│   ├── tests/
│   │   ├── test_forms.py
│   │   ├── test_models.py
│   │   ├── test_permissions.py
│   │   └── test_views.py
│   │
│   ├── admin.py
│   ├── apps.py
│   ├── mixins.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── manage.py
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone git@github.com:VGrechkosij/django-crm-system.git
cd django-crm-system
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Apply migrations and create a superuser:

```bash
python manage.py migrate
python manage.py createsuperuser
```

Run the development server:

```bash
python manage.py runserver
```

Open the project:

```text
http://127.0.0.1:8000/
```

---

## Running Tests

Run all tests:

```bash
python manage.py test
```

Run tests for the CRM app:

```bash
python manage.py test crm
```

---

## Code Quality

Run Django system checks:

```bash
python manage.py check
```

Run Flake8:

```bash
flake8 crm config manage.py
```

---

## Tests Coverage

The project includes tests for important backend logic:

- Model methods and default values
- Forms
- Role-based permissions
- Comment permissions
- Automatic field assignment in views

Examples of tested logic:

- Client manager is set automatically
- Task creator is set automatically
- Deal manager is set automatically
- Task comment author and task are set automatically
- Users see only objects allowed by their role

---

## Database Query Optimization

The project uses query optimization in list and detail views:

- `select_related()` for foreign key relationships
- `prefetch_related()` for task comments and authors

This helps reduce unnecessary database queries when rendering related objects in templates.

---

## Future Improvements

Planned improvements:

- Add Django REST Framework API
- Add JWT authentication
- Add Swagger/OpenAPI documentation
- Add PostgreSQL
- Add Docker
- Add deployment configuration
- Add API tests
- Add CI/CD pipeline

---

## Author

Created by Vlad Grechkosij as a Django backend pet project.
