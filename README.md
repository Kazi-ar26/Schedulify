# ✦ Schedulify v2.0

> **Intelligent academic planning and productivity management for students.**

Schedulify is a student productivity platform designed to help students organize academic tasks, manage deadlines, plan study sessions, and monitor their productivity through intelligent scheduling and analytics.

The application also provides teachers with class-level insights to help understand overall academic progress and productivity.

---

## Architecture

```
Desktop App (PySide6)
        ↓ HTTPS
FastAPI Backend
        ↓ SQLAlchemy
PostgreSQL (Supabase)
```

```
Schedulify v2.0
│
├── backend/              # FastAPI REST API
│   ├── main.py           # Application entry point
│   ├── database.py       # PostgreSQL engine/session
│   ├── security.py       # JWT auth, password hashing
│   ├── schemas.py        # Pydantic request/response models
│   └── routes/           # API endpoint modules
│       ├── auth.py       # Registration, login, profile
│       ├── tasks.py      # Task CRUD
│       ├── schedules.py  # Schedule management, AI generation
│       ├── calendar.py   # Calendar events
│       ├── analytics.py  # Student & teacher analytics
│       ├── notifications.py
│       ├── settings.py   # User preferences
│       └── users.py      # User profile
│
├── api_client/           # Desktop HTTP client
│   ├── client.py         # HTTP client with JWT storage
│   ├── auth_api.py       # Auth API calls
│   ├── tasks_api.py      # Task API calls
│   ├── schedules_api.py  # Schedule API calls
│   ├── analytics_api.py  # Analytics API calls
│   ├── calendar_api.py   # Calendar API calls
│   ├── notifications_api.py
│   └── settings_api.py   # Settings API calls
│
├── models/               # Shared SQLAlchemy ORM models
│   ├── user.py           # User (student/teacher auth)
│   ├── student.py        # Student profile
│   ├── teacher.py        # Teacher profile
│   ├── task.py           # Tasks with priorities
│   ├── schedule.py       # AI-generated schedules
│   ├── calendar_event.py # Calendar entries
│   ├── notification.py   # Notifications
│   ├── productivity.py   # Productivity tracking
│   ├── analytics.py      # Analytics records
│   └── setting.py        # User settings
│
├── controllers/          # Application logic
├── services/             # Business logic
├── ai_engine/            # Smart scheduling & predictions
├── ui/                   # PySide6 desktop UI
│   ├── login/            # Auth screens
│   ├── student/          # Student views
│   ├── teacher/          # Teacher views
│   ├── components/       # Reusable UI components
│   └── settings/         # Settings & theme
│
├── styles/               # QSS stylesheets
├── tests/                # Pytest test suite
├── config.py             # Configuration loader
├── config.json           # Application configuration
└── main.py               # Desktop application entry point
```

---

## Features

### Student Features
- **Smart Scheduling** — AI-powered task scheduling based on priority, deadlines, and working hours
- **Automatic Rescheduling** — Dynamic schedule adjustment when tasks are missed or moved
- **Task Management** — Create, prioritize, track, and manage academic tasks
- **Calendar** — View scheduled tasks and events in an integrated calendar
- **Productivity Analytics** — Track study sessions, completion rates, and trends
- **Wellbeing Indicators** — Non-clinical productivity balance insights
- **Cross-Device Access** — Log in from any device with the same account

### Teacher Features
- **Class Dashboard** — Aggregated class productivity overview
- **Class Analytics** — Completion rates, focus time, and workload metrics
- **Anonymous Reports** — Privacy-safe aggregated student insights
- **No individual student data is exposed**

### General
- **Modern UI** — Clean, professional dark/light theme interface
- **JWT Authentication** — Secure token-based login sessions
- **Persistent Accounts** — Registration survives application restarts
- **Role-Based Access** — Separate student and teacher experiences

---

## Technology

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Desktop UI | PySide6 (Qt6) |
| Backend API | FastAPI |
| Database | PostgreSQL (Supabase) |
| ORM | SQLAlchemy 2.0 |
| Auth | JWT + bcrypt |
| HTTP Client | httpx |
| Visualization | PyQtGraph |
| Styling | Qt Style Sheets (QSS) |
| Packaging | PyInstaller |

---

## Getting Started

### Prerequisites
- Python 3.12+
- PostgreSQL database (or Supabase)
- Git

### Clone

```bash
git clone https://github.com/Kazi-ar26/Schedulify.git
cd Schedulify
```

### Install Dependencies

```bash
python -m pip install -r Requirements.txt
```

### Environment Setup

Create a `.env` file (see `.env.example`):

```env
# Backend Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/schedulify

# JWT Secret (change in production!)
SCHEDULIFY_SECRET_KEY=your-secret-key-here

# Desktop API URL
SCHEDULIFY_API_URL=http://localhost:8000
```

### Run the Backend

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

The API docs are available at: `http://localhost:8000/docs`

### Run the Desktop App

In a separate terminal:

```bash
python main.py
```

---

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register` | Create new account |
| POST | `/api/auth/login` | Get JWT token |
| GET | `/api/auth/me` | Get current user profile |

### Tasks
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/tasks` | List tasks |
| POST | `/api/tasks` | Create task |
| PUT | `/api/tasks/{id}` | Update task |
| DELETE | `/api/tasks/{id}` | Delete task |
| POST | `/api/tasks/{id}/complete` | Mark complete |

### Schedules
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/schedules` | List schedules |
| POST | `/api/schedules` | Create schedule |
| POST | `/api/schedules/generate` | AI generate schedule |
| POST | `/api/schedules/{id}/complete` | Mark complete |

### Calendar
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/calendar` | List events |
| POST | `/api/calendar` | Create event |
| DELETE | `/api/calendar/{id}` | Delete event |

### Analytics
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/analytics/student` | Student summary |
| GET | `/api/analytics/productivity` | Productivity records |
| POST | `/api/analytics/productivity` | Create record |
| GET | `/api/analytics/teacher` | Class statistics |

### Other
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/notifications` | List notifications |
| POST | `/api/notifications/read-all` | Mark all read |
| GET | `/api/settings` | Get settings |
| PUT | `/api/settings` | Update settings |
| GET | `/api/health` | Health check |

---

## Database Setup

### Supabase (Recommended)

1. Create a Supabase project at [supabase.com](https://supabase.com)
2. Go to Settings → Database and copy the connection string
3. Set `DATABASE_URL` in your `.env`:

```
DATABASE_URL=postgresql://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres
```

### Local PostgreSQL

```bash
createdb schedulify
export DATABASE_URL=postgresql://localhost:5432/schedulify
```

Tables are created automatically on first backend startup.

---

## Running Tests

```bash
python -m pytest tests/ -v
```

Tests cover:
- Authentication (register, login, password hashing, JWT)
- Database operations (CRUD, relationships)
- Service layer (tasks, notifications, analytics, wellbeing, settings)
- Smart scheduler (priority, working hours, conflicts)
- API client operations

---

## Building Windows Executable

```bash
python -m PyInstaller Schedulify.spec
```

The executable is created in the `dist/` folder.

---

## Project Structure

- `backend/` — FastAPI REST API (deployed separately)
- `api_client/` — Desktop HTTP client (replaces direct DB access)
- `models/` — Shared SQLAlchemy ORM models
- `controllers/` — Application logic layer
- `services/` — Business logic layer
- `ai_engine/` — Smart scheduling & prediction algorithms
- `ui/` — PySide6 desktop interface
- `styles/` — QSS theme stylesheets
- `tests/` — Pytest test suite

---

## Security Notes

- Passwords are hashed with bcrypt
- API uses JWT tokens (24-hour expiry)
- Database credentials stay server-side only
- Desktop communicates via HTTPS to backend
- No secrets stored in desktop application
- Teacher analytics are aggregated and anonymized

---

## Known Limitations

- The AI scheduler is algorithmic (priority-based), not ML-powered
- Calendar events are manual (no external calendar sync yet)
- Notifications are in-app only (no push notifications)
- Single-tenant deployment (no multi-school admin panel)

---

## Roadmap

- [ ] Google Calendar integration
- [ ] Google Classroom integration
- [ ] Push notifications
- [ ] Enhanced ML scheduling
- [ ] Multi-school admin panel
- [ ] Mobile companion app
- [ ] Docker deployment
- [ ] CI/CD pipeline

---

## License

This project is developed as an educational software project.

---

<p align="center">
  <strong>✦ Schedulify v2.0</strong><br>
  Plan smarter. Study better. Stay on track.
</p>
