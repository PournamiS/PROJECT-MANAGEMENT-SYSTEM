# Project Management System

A Django-based web application to manage projects, tasks, and users with role-based access control.

## Tech Stack
- Python 3.10+
- Django 4.2.7
- MySQL
- Bootstrap 5
- Bootstrap Icons

## Roles
| Role      | Permissions                                      |
|-----------|--------------------------------------------------|
| Admin     | Full CRUD on users, projects, tasks              |
| Developer | View assigned projects, update own task status   |

## Setup Instructions

### 1. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create MySQL database
```sql
CREATE DATABASE project_management_db;
```

### 4. Update database settings
Edit `project_management/settings.py` and set your MySQL password:
```python
'PASSWORD': 'your_actual_password',
```

### 5. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create admin user
```bash
python manage.py createsuperuser
```
Then set the role to admin via Django shell:
```bash
python manage.py shell
>>> from core.models import User
>>> u = User.objects.get(username='your_username')
>>> u.role = 'admin'
>>> u.save()
>>> exit()
```

### 7. Run the server
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

## Project Structure
```
project_management/
├── core/
│   ├── models.py       # User, Project, Task models
│   ├── views.py        # All views
│   ├── urls.py         # URL routing
│   ├── forms.py        # Django forms
│   ├── admin.py        # Admin panel config
│   └── decorators.py   # Auth decorators
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── dashboard/
│   ├── projects/
│   ├── tasks/
│   └── users/
├── project_management/
│   ├── settings.py
│   └── urls.py
├── manage.py
└── requirements.txt
```
