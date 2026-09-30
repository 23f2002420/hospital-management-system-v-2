# 🏥 Hospital Management System

A full-stack **Hospital Management System (HMS)** designed to simplify and manage hospital operations through a web-based platform.

The system provides separate dashboards and functionality for **Administrators, Doctors, and Patients**, allowing users to manage appointments, doctors, patients, departments, availability, medical history, and other hospital-related activities.

---

## 🚀 Features

### 👨‍💼 Admin

* Admin authentication and authorization
* Admin dashboard
* Manage doctors
* Manage patients
* Manage departments
* View and manage appointments
* Monitor hospital activities
* Manage doctor availability

### 👨‍⚕️ Doctor

* Doctor authentication
* Doctor dashboard
* View appointments
* Manage appointment status
* View patient information
* View patient history
* Manage availability
* Update personal profile
* Access appointment details

### 🧑‍🦱 Patient

* Patient registration and login
* Patient dashboard
* Search/view doctors
* Book appointments
* Reschedule appointments
* View appointment history
* View treatment/medical history
* Update profile
* Export treatment history
* Receive notifications related to appointments

---

## ⚙️ Advanced Features

The project also includes background task processing using **Celery**.

Current background-task functionality includes:

* Patient treatment-history export
* Email notifications
* Daily appointment reminders
* Monthly doctor reports
* Asynchronous background processing

The project uses a local SMTP server configuration for development/testing.

---

## 🛠️ Technology Stack

### Frontend

* Vue.js
* JavaScript
* HTML
* CSS
* Vue Router
* Axios
* npm

### Backend

* Python
* Flask
* Flask-SQLAlchemy
* Flask-JWT-Extended
* Flask-Security
* REST APIs

### Database

* SQLite
* SQLAlchemy ORM

### Background Processing

* Celery
* Redis/message broker
* SMTP for email functionality

### Development Environment

* Windows / WSL
* Ubuntu
* Git & GitHub
* VS Code

---

## 📂 Project Structure

```text
hospital-management-system-v-2/
│
├── Frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── routes.js
│   │   └── ...
│   ├── package.json
│   └── package-lock.json
│
├── backend/
│   ├── application/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   ├── security.py
│   │   ├── celery_init.py
│   │   ├── mail.py
│   │   └── tasks.py
│   │
│   ├── instance/
│   │   └── hmsDb.sqlite3
│   │
│   ├── app.py
│   ├── celery_config.py
│   ├── requirements.txt
│   └── endpoints.txt
│
└── README.md
```

---

# 💻 Installation & Setup

## 1. Clone the repository

```bash
git clone https://github.com/23f2002420/hospital-management-system-v-2.git
cd hospital-management-system-v-2
```

---

# 🔧 Backend Setup

Move into the backend directory:

```bash
cd backend
```

Create a Python virtual environment:

```bash
python3 -m venv venv
```

Activate it:

### Linux / WSL

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the Flask backend:

```bash
python app.py
```

The backend will normally be available at:

```text
http://127.0.0.1:5000
```

---

# 🎨 Frontend Setup

Open another terminal and move to the frontend:

```bash
cd Frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run serve
```

The frontend will normally be available at:

```text
http://localhost:8080
```

---

# 🔐 Authentication

The application uses token-based authentication and role-based access control.

Users are separated into different roles:

```text
Admin
Doctor
Patient
```

Each role has access to its own dashboard and permitted functionality.

---

# 📨 Email & Background Tasks

The project contains asynchronous background functionality using Celery.

Examples include:

```text
Patient
   │
   │ Request treatment history export
   ▼
Flask API
   │
   ▼
Celery Task
   │
   ▼
Generate CSV
   │
   ▼
Send Email
```

For development, the email system is configured to work with a local SMTP server.

Celery-related files:

```text
backend/
├── celery_config.py
└── application/
    ├── celery_init.py
    ├── mail.py
    └── tasks.py
```

---

# 📋 API

The backend provides REST APIs for operations such as:

* Authentication
* Patient management
* Doctor management
* Department management
* Appointment management
* Doctor availability
* Patient history
* Profile management
* Background task processing

Additional endpoint information can be found in:

```text
backend/endpoints.txt
```

---

# 🗄️ Database

The project currently uses **SQLite** with SQLAlchemy.

Database file:

```text
backend/instance/hmsDb.sqlite3
```

The database contains information related to:

* Users
* Patients
* Doctors
* Departments
* Appointments
* Treatments
* Availability
* Authentication/roles

---

# 🧪 Development

This project was developed and tested using a local development environment.

Recommended setup:

```text
Python 3
Node.js
npm
SQLite
Git
WSL/Ubuntu or Windows
```

---

# 🔮 Future Improvements

Possible future enhancements include:

* Online payment integration
* Video consultation
* Prescription management
* Advanced analytics dashboard
* Hospital billing system
* SMS notifications
* Cloud database integration
* Production email service
* Docker deployment
* Cloud deployment
* Automated testing and CI/CD
* AI-assisted medical appointment management

---

# 🎯 Project Goals

The main goal of this project is to provide a centralized platform for managing common hospital operations while reducing manual work.

It demonstrates the development of a complete full-stack application involving:

**Frontend → REST API → Backend → Database → Authentication → Background Tasks → Email Notifications**

---

# 👨‍💻 Author

**Rehan Alam**

GitHub:
https://github.com/23f2002420

---

## ⭐ Contributing

Contributions, suggestions, and improvements are welcome.

If you find an issue or have an idea for improving the project, feel free to open an issue or submit a pull request.

---

## 📄 License

This project is intended primarily for educational and portfolio purposes.
