# ✦ Schedulify

> **Intelligent academic planning and productivity management for students.**

Schedulify is a desktop productivity application designed to help students organize academic tasks, manage deadlines, plan study sessions, and monitor their productivity through intelligent scheduling and analytics.

The application also provides teachers with class-level insights to help understand overall academic progress and productivity.

---

## Features

* **Smart Scheduling**
  Automatically schedules tasks around deadlines, priorities, estimated durations, and available time.

* **Automatic Rescheduling**
  Dynamically reorganizes upcoming tasks when schedules change or tasks are missed.

* **Task Management**
  Create, prioritize, track, and manage academic tasks and deadlines.

* **Calendar**
  View scheduled tasks and events in an integrated calendar interface.

* **Productivity Analytics**
  Visualize completion rates, productivity trends, and study patterns.

* **Student Dashboard**
  Provides an overview of upcoming work, schedules, deadlines, and productivity.

* **Teacher Dashboard**
  Provides class-level analytics and anonymous productivity insights.

* **Themes & UI**
  Modern desktop interface with light and dark themes.

---

## Technology

| Layer           | Technology            |
| --------------- | --------------------- |
| Language        | Python 3.12           |
| UI              | PySide6               |
| Database        | MySQL                 |
| ORM             | SQLAlchemy            |
| Database Driver | PyMySQL               |
| Visualization   | PyQtGraph             |
| Styling         | Qt Style Sheets (QSS) |
| Packaging       | PyInstaller           |

---

## Architecture

Schedulify follows a modular architecture separating the user interface, business logic, database layer, and scheduling engine.

```text
Schedulify
│
├── UI
│   ├── Student
│   ├── Teacher
│   ├── Components
│   └── Dialogs
│
├── Controllers
│   └── Application Logic
│
├── Services
│   ├── Task Management
│   ├── Scheduling
│   └── Calendar
│
├── AI Engine
│   ├── Smart Scheduler
│   └── Rescheduler
│
└── Database
    ├── Models
    ├── Sessions
    └── Migrations
```

---

## Getting Started

### Requirements

* Python 3.12+
* MySQL Server
* Git

### Installation

Clone the repository:

```bash
git clone https://github.com/Kazi-ar26/Schedulify.git
cd Schedulify
```

Install the required dependencies:

```bash
python -m pip install -r requirements.txt
```

Configure the MySQL database using `config.json`, then start the application:

```bash
python main.py
```

---

## Project Status

**Active Development**

Schedulify is currently under active development, with ongoing improvements to scheduling, analytics, teacher functionality, UI/UX, and deployment.

---

## Roadmap

* [ ] Google Calendar integration
* [ ] Google Classroom integration
* [ ] Cloud database support
* [ ] Enhanced scheduling algorithms
* [ ] Expanded teacher analytics
* [ ] Cross-platform distribution

---

## License

This project is currently developed as an educational software project. Licensing information will be added prior to public release.

---

<p align="center">
  <strong>✦ Schedulify</strong><br>
  Plan smarter. Study better. Stay on track.
</p>
