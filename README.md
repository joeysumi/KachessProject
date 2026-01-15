# KachessProject
A trip/event planning and facilitating tool.

<sub>Django 6.0 project using Python 3.13.</sub>

## Project Structure

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

## App Vocabulary (not necessarily front-facing)
* organization - A church, family, or company. This is the base structure from where a trip is attached.
Each organization can contain multiple <i>contacts</i>.
* trip - A trip/event to be planned. You can plan trip details, collaborate with attendees, and facilitate the trip while you're on the go.
* user - A registered account attached to >1 organization.
