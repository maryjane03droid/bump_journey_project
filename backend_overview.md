# BumpJourney Backend Project Overview

## Project Purpose
BumpJourney is a Django REST API backend for a maternity care platform that helps expectant mothers record health data and allows medical staff to review patient information, appointments, and clinical notes.

## Core Technology Stack
- Python
- Django
- Django REST Framework (DRF)
- SimpleJWT for authentication
- PostgreSQL or SQLite via environment configuration
- CORS enabled for frontend integration

## Main Project Structure
- `manage.py` – Django project entry point
- `bump_journey/` – project settings, root URL routing, WSGI/ASGI config
- `accounts/` – user authentication, registration, profiles, and user roles
- `tracker/` – pregnancy details and health log tracking
- `staff/` – appointments, staff notes, and clinical workflows

## Key Backend Apps

### 1. Accounts App
Responsibilities:
- Custom user model with roles such as PATIENT, DOCTOR, MIDWIFE, and NURSE
- User registration and login
- JWT token-based authentication
- Patient profile management

Main files:
- `accounts/models.py`
- `accounts/views.py`
- `accounts/serializers.py`
- `accounts/urls.py`

### 2. Tracker App
Responsibilities:
- Pregnancy profile creation and updates
- Daily health log recording
- Monitoring of symptoms, blood pressure, weight, and fetal movement
- Optional urgent-attention flag on health logs

Main files:
- `tracker/models.py`
- `tracker/views.py`
- `tracker/serializers.py`
- `tracker/urls.py`

### 3. Staff App
Responsibilities:
- Appointment management
- Staff notes and prescriptions
- Clinical follow-up workflow for caregivers

Main files:
- `staff/models.py`
- `staff/views.py`
- `staff/serializers.py`
- `staff/urls.py`

## API Design
The backend exposes REST APIs under the `/api/` prefix:
- `/api/accounts/` – authentication, profile, and account management
- `/api/tracker/` – pregnancy profiles and health logs
- `/api/staff/` – appointments and staff notes

## Authentication Flow
1. A user registers or logs in.
2. The server returns JWT access and refresh tokens.
3. The client sends the access token in the Authorization header.
4. Protected endpoints are accessible only to authenticated users.

## Data Model Summary
Important models include:
- `User` – custom Django user with role support
- `PatientProfile` – basic patient profile details
- `PregnancyProfile` – pregnancy-specific information and estimated due date
- `HealthLog` – patient health monitoring entries
- `Appointment` – scheduled or requested medical appointments
- `StaffNote` – documentation created by staff for a patient

## Notes on the Current State
- The project is structured as a modular Django backend with clear app separation.
- Some models and concepts appear to overlap across apps, which may indicate an evolving architecture.
- The API is already designed to support both patients and staff roles.

## Typical Development Workflow
- Install dependencies from `requirements.txt`
- Run migrations
- Start the server with Django
- Test endpoints through DRF or frontend integration

## Suggested Next Steps
- Review and consolidate duplicated models where appropriate
- Add permission rules for role-based access control
- Expand testing coverage for the API endpoints
- Document endpoint examples and expected payloads more thoroughly
