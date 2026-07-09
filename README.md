 (Bump Journey)

A full-stack maternal health management system connecting expectant mothers with healthcare professionals. Built for real-time health tracking, appointment management, clinical collaboration, and care continuity.

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React, Tailwind CSS, React Icons, Google Fonts |
| Backend | Django, Django REST Framework, SimpleJWT |
| Database | PostgreSQL (Render) |
| Auth | JWT (Access + Refresh tokens) |

## 👥 User Roles

| Role | Access Level |
|------|-------------|
| Patient | Register, create profile, track vitals, request appointments, view audit trail |
| Doctor / Pediatrician / Nurse | Attend patients directly, schedule appointments, refer cases, lock cases |
| Midwife / Nutritionist / Lab Technician / Therapist | Receive referrals only from primary staff |
| Admin | Approve staff, review career applications, manage users, handle contact messages |

## 🔒 Authentication Flow

1. Client submits credentials to `/api/accounts/login/`
2. Server validates and issues `access` + `refresh` JWT tokens
3. Unapproved staff are blocked at login with a pending message
4. Tokens stored in `localStorage`, attached as `Bearer` in request headers
5. Token refresh via `/api/accounts/token/refresh/`

## 📡 API Endpoints

### Accounts
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/accounts/register/` | Patient registration |
| POST | `/api/accounts/register/staff/` | Staff registration (requires admin approval) |
| POST | `/api/accounts/login/` | JWT login |
| POST | `/api/accounts/token/refresh/` | Refresh access token |
| GET | `/api/accounts/admin/users/` | Admin: list all users (filterable by ?role=) |
| PATCH | `/api/accounts/admin/users/<id>/approve/` | Admin: approve/reject staff |
| POST | `/api/accounts/careers/apply/` | Submit career application |
| GET | `/api/accounts/admin/careers/` | Admin: view applications |
| POST | `/api/accounts/contact/` | Send contact message |
| GET | `/api/accounts/admin/messages/` | Admin: view contact messages |

### Tracker
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/tracker/pregnancy-profiles/` | Patient profile CRUD |
| GET/POST | `/api/tracker/health-logs/` | Daily vitals CRUD |
| PUT/DELETE | `/api/tracker/health-logs/<id>/` | Update/delete vitals |

### Staff
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/staff/appointments/` | Appointment CRUD |
| POST | `/api/staff/appointments/<id>/refer/` | Refer case to another staff |
| POST | `/api/staff/appointments/<id>/lock/` | Lock case to prevent access by others |
| GET/POST | `/api/staff/notes/` | Staff clinical notes CRUD |
| GET | `/api/staff/audit-trail/` | View audit trail |
| GET | `/api/staff/patients/` | Staff: list all patients |

## 🏥 Key Features

- **Patient Profile**: Auto-calculates estimated due date from last menstrual period
- **Daily Vitals**: Blood pressure, weight, temperature, kick count, symptoms (dropdown + other), mood (optional)
- **Appointment System**: Patients request, staff schedule with date/time
- **Case Locking**: Once a staff member opens a case, others are blocked with a message
- **Referral System**: Primary staff refer to specialists with status tracking
- **Audit Trail**: Every action recorded (who did what, when, to which patient)
- **Career Applications**: Public users apply for staff roles, admin reviews and approves
- **Contact Messages**: Public contact form, admin receives and responds

## 🚀 Setup

### Prerequisites
- Python 3.10+
- PostgreSQL
- Node.js 18+ (for frontend)

### Backend Setup

```bash
git clone https://github.com/maryjane03droid/bump_journey_project.git
cd bump_journey_project
python -m venv .venv
source .venv/Scripts/activate  # Windows Git Bash
pip install -r requirements.txt