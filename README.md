# BumpJourney - Full-Stack Maternity Care Tracking System

A full-stack web application designed to connect expectant mothers with medical professionals, allowing real-time symptom recording, health metrics documentation, and clinical care collaboration.

## 🛠️ Tech Stack
- **Frontend:** React.js, React Router, Context/Local Storage Token Management
- **Backend:** Django, Django REST Framework (DRF), SimpleJWT Authentication
- **Database:** PostgreSQL / SQLite

## 🔒 Authentication Flow
This system enforces strict JWT stateless authentication:
1. Client submits credentials (`username`, `password`) to `/api/accounts/login/`.
2. Server issues short-lived `access` token and long-lived `refresh` token.
3. Client stores tokens securely in `localStorage` and embeds the bearer token in headers for protected routes.