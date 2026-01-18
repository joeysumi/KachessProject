# KachessProject
A trip/event planning and facilitating tool.

<<<<<<< HEAD
A trip/event planning and facilitating tool.

<sub>Django 6.0 project using Python 3.13.<sub>

## History

<sub>Pronunciation: ka-CHEES<sub>

Lake Kachess is a resevoir in the Cascade Mountains in Washington state. For almost three decades my family has anually met to camp along it's shoreline. Originally this project was inspired by the burden to plan such an event that started with a measy group of five to some years up to 25!

Simultaneously, I have organized, hosted, and participated in multiple short-term church mission trips. I realized that a single tool could aid in the planning and execution of both styles of trips.

## Key elements

- Trip participants may add/view/change certain information without needing to create their own account.
- The base level is organization. All users and trips must be associated with at least one organization.
- Each organization has it's own list of people, and trips select persons from that organization-level list.

### Future Considerations Not Currently Planned

- Organizations can share trips with another organization
- Users have their own user-level dashboard (i.e. a single page displaying trips & other information across all organizations)

## Project Structure

```
KACHESS PROJECT
├── config
├── organizations
│   ├── migrations
│   ├── models
│   └── tests
│       └── factories
└── trips
    ├── migrations
    ├── models
    └── tests
        └── factories
```

<sub>Modified: 2026-01-17<sub>
=======
<sub>Django 6.0 project using Python 3.13.</sub>

## Project Structure
>>>>>>> 79b2a3a9ec54618be9b6648dd2e1374da2525581

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

<<<<<<< HEAD
## App Terminology (not necessarily the front-facing vocabulary)

- organization - A church, family, or company. This is the base structure from where a trip is attached.
  Each organization can contain multiple <i>contacts</i>.
- trip - A trip/event to be planned. You can plan trip details, collaborate with attendees, and facilitate the trip while you're on the go.
- user - A registered account attached to 1 or more organizations.
- person - Someone associated with the organization. From this list, an organizer can add participants or when new participants are added, the names
  and information are ultimately saved as a part of the organization.

## Special Relationships

### user_profile

Since a user can (and should) be considered a person in the organization - and can be a trip participant - they would have personal data like other "persons."

However, I didn't want to burden a user with duplication over more than one organizations that they are a part of and therefore I created the user_profile model - each user has a person profile - one single source of truth.

### Organization Permissions

At this point there are three permissions for a user account for an organization:

- admin - read, write, delete
- organizer - read, write
- observer - read

### Trip Statues

There are currently three statuses a person can have on a trip:

- interested
- considering
- attending

A trip status has nothing to do with permissions, but helps the trip organizer classify a person's involvement in the trip.
=======
## App Vocabulary (not necessarily front-facing)
* organization - A church, family, or company. This is the base structure from where a trip is attached.
Each organization can contain multiple <i>contacts</i>.
* trip - A trip/event to be planned. You can plan trip details, collaborate with attendees, and facilitate the trip while you're on the go.
* user - A registered account attached to >1 organization.
>>>>>>> 79b2a3a9ec54618be9b6648dd2e1374da2525581
