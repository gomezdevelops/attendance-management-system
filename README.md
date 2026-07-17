<div align="center">

# 🎓 Smart Attendance and Monitoring System

### Real-time facial recognition attendance for the modern classroom

A web-based attendance management system that replaces manual roll calls with automated facial recognition, role-based authentication, attendance analytics, and automated email notifications.

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-5C3EE8?logo=opencv&logoColor=white)](https://opencv.org/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-07405E?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![License: Educational](https://img.shields.io/badge/License-Educational-yellow.svg)](#license)

[Overview](#-overview) • [Features](#-key-features) • [Architecture](#-system-architecture) • [Getting Started](#-getting-started) • [Roadmap](#-future-enhancements)

</div>

---

## 📖 Overview

**Smart Attendance and Monitoring System** is a full-stack web application built as a Bachelor of Computer Applications (BCA) major project. It automates classroom attendance using real-time facial recognition, eliminating manual roll calls and proxy attendance.

Admins register students, manage subjects, and run live attendance sessions where the system identifies students through a webcam feed and logs attendance automatically. Students log in to a dedicated portal to track their attendance percentage per subject, and the system proactively emails students who fall below the required threshold.

**Why it matters:**
- ⏱️ Cuts attendance-taking time from minutes to seconds
- 🚫 Prevents proxy attendance ("buddy punching") through face verification
- 📊 Gives administrators real-time visibility into attendance trends
- 📬 Automatically flags and notifies at-risk students, no manual tracking required

---

## ✨ Key Features

### 👨‍💼 Admin Portal
| Feature | Description |
|---|---|
| Secure Authentication | Session-based admin login |
| Student Management | Add, edit, and remove student records |
| Subject Management | Create and organize subjects/classes |
| Face Registration | Capture and enroll student face data |
| Attendance Sessions | Start/stop live recognition sessions per class |
| Reports & Analytics | Generate attendance summaries and trends |
| Data Export | Export attendance to CSV / Excel |
| Email Alerts | Send low-attendance warnings and absence notices |

### 👨‍🎓 Student Portal
- Secure roll-number based login
- View overall and subject-wise attendance percentage
- Track real-time attendance status

### 🤖 Face Recognition Engine
- Real-time face detection via webcam
- Deep-learning-based face encoding and matching
- Automatic attendance marking on match
- Duplicate-entry prevention within the same session

### 📧 Notification System
- Automated absence emails
- Low-attendance (**< 75%**) warning emails
- Full email activity logging for audit purposes

---

## 🏗 System Architecture

```
┌─────────────────────────────────────────┐
│           Presentation Layer             │
│      HTML5 • CSS3 • JavaScript • BS      │
└───────────────────┬───────────────────────┘
                     │
┌─────────────────────────────────────────┐
│           Flask Web Application          │
├───────────┬───────────┬─────────┬───────┤
│   Auth    │Attendance │ Reports │ Email │
│  Service  │  Service  │ Service │Service│
└───────────┴───────────┴─────────┴───────┘
                     │
┌─────────────────────────────────────────┐
│        Face Recognition Engine           │
│      OpenCV • face_recognition • NumPy   │
└───────────────────┬───────────────────────┘
                     │
┌─────────────────────────────────────────┐
│           SQLite Database                │
└─────────────────────────────────────────┘
```

---

## 🛠 Technology Stack

| Layer | Technologies |
|---|---|
| **Backend** | Python, Flask |
| **Frontend** | HTML5, CSS3, JavaScript, Bootstrap |
| **Computer Vision** | OpenCV, `face_recognition`, NumPy |
| **Database** | SQLite |
| **Reporting** | Pandas |
| **Email Service** | Gmail SMTP |

---

## 📂 Project Structure

```text
smart-attendance-system/
├── app.py                 # Application entry point
├── config.py               # App configuration & environment settings
├── requirements.txt         # Python dependencies
│
├── database/                # SQLite database files
├── dataset/                  # Captured face image data
├── logs/                       # Application & email logs
│
├── models/                     # Data models / ORM schemas
├── routes/                      # Flask route handlers (blueprints)
├── services/                     # Business logic (auth, attendance, email, face recognition)
├── utils/                          # Shared helper functions
│
├── templates/                       # Jinja2 HTML templates
└── static/                           # CSS, JS, images
```

---

## 📊 Database Design

The system is built around six core entities:

| Entity | Purpose |
|---|---|
| **Admin** | Administrator credentials and access control |
| **Students** | Student profiles and roll numbers |
| **Subjects** | Course/subject definitions |
| **Attendance** | Daily attendance records per student/subject |
| **Face Encodings** | Stored facial embeddings for recognition |
| **Email Logs** | History of sent notifications |

---

## 🔄 System Workflow

1. Administrator logs into the system
2. Student information is registered
3. Facial images are captured for enrollment
4. Face encodings are generated and stored
5. Administrator starts an attendance session for a subject
6. Webcam captures live video of the classroom
7. Students are identified in real time via facial recognition
8. Attendance is automatically recorded (duplicates prevented)
9. Daily and periodic reports are generated
10. Automated emails are sent for absences and low attendance
11. Students log in anytime to monitor their attendance status

---

## 🔐 Authentication

The application uses **role-based authentication** with two distinct portals:

| Role | Credentials |
|---|---|
| **Administrator** | Username + Password |
| **Student** | Roll Number + Password |

All passwords are securely stored using password hashing. Plaintext credentials are never persisted.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- A working webcam
- Gmail account (for SMTP email notifications)

### 1. Clone the repository
```bash
git clone https://github.com/gomezdevelops/attendance-management-system.git
cd attendance-management-system
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment settings
Update `config.py` (or a `.env` file, if used) with your database path and Gmail SMTP credentials for email notifications.

### 5. Run the application
```bash
python app.py
```

The app will start locally. Open the URL shown in your terminal (typically `http://127.0.0.1:5000`) to access it.

---

## 🎯 Project Objectives

- ✅ Automate attendance marking with facial recognition
- ✅ Prevent proxy/buddy attendance
- ✅ Improve attendance accuracy and consistency
- ✅ Reduce manual administrative workload
- ✅ Provide actionable attendance analytics
- ✅ Automatically notify students of absences and low attendance
- ✅ Improve overall administrative efficiency

---

## 📜 License

This project was developed for educational purposes as part of my **Bachelor of Computer Applications (BCA) Major Project**. It is free to use and modify for learning purposes.

---

<div align="center">

⭐ **If you found this project useful, consider giving it a star!** ⭐

</div>
