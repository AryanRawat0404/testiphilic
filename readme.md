# Online Test Management System

A Django-based web application for managing online tests for schools.

## Features
- Role-based login (Admin / Teacher / Student)
- Teachers can create tests with start & end time
- Students can attempt tests within allowed time
- Auto test visibility using start/end time
- Prevent multiple submissions per subject
- Admin panel support (Django built-in)

## Tech Stack
- Django
- SQLite (development)
- HTML / CSS

## Setup
```bash
git clone https://github.com/your-username/project-name.git
cd Testiphilic
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
