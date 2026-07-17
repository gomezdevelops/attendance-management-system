# 🎓 Smart Attendance and Monitoring System using Face Recognition

> A modern web-based attendance management system that automates classroom attendance using real-time facial recognition, role-based authentication, attendance analytics, and automated email notifications.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.x-black?logo=flask)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green?logo=opencv)
![SQLite](https://img.shields.io/badge/Database-SQLite-blue?logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📖 Overview

The **Smart Attendance and Monitoring System using Face Recognition** is a web-based application developed as a **Bachelor of Computer Applications (BCA) Major Project**.

The system replaces traditional attendance methods with an automated facial recognition solution, reducing manual effort, preventing proxy attendance, and providing administrators with comprehensive attendance reports and monitoring tools.

Students can securely log in to monitor their attendance percentage, while administrators can manage attendance sessions, generate reports, and send automated email notifications.

---

## ✨ Key Features

### 👨‍💼 Admin Portal

- Secure authentication
- Student management
- Subject management
- Face registration
- Attendance session management
- Attendance report generation
- Attendance analytics
- Export reports (CSV / Excel)
- Send low attendance warning emails
- Send absence notifications

---

### 👨‍🎓 Student Portal

- Secure login
- View attendance percentage
- View subject-wise attendance
- Monitor attendance status

---

### 🤖 Face Recognition

- Real-time face detection
- Face encoding generation
- Face matching using Deep Learning
- Automatic attendance marking
- Duplicate attendance prevention

---

### 📧 Notification System

- Automated absence emails
- Low attendance (<75%) warning emails
- Email activity logging

---

## 🏗 System Architecture

The application follows a layered architecture.

```
Presentation Layer
        │
        ▼
HTML • CSS • JavaScript
        │
        ▼
Flask Web Application
        │
 ┌──────┼─────────┐
 │      │         │
 ▼      ▼         ▼
Authentication
Attendance
Reports
Email Service
Face Recognition
        │
        ▼
SQLite Database
```

---

## 🛠 Technology Stack

### Backend

- Python
- Flask

### Frontend

- HTML5
- CSS3
- JavaScript
- Bootstrap

### Computer Vision

- OpenCV
- face_recognition
- NumPy

### Database

- SQLite

### Reporting

- Pandas

### Email Service

- Gmail SMTP

---

## 📂 Project Structure

```text
smart-attendance-system/

├── app.py
├── config.py
├── requirements.txt
│
├── database/
├── dataset/
├── logs/
│
├── models/
├── routes/
├── services/
├── utils/
│
├── templates/
└── static/
```

---

## 📊 Database Design

The system consists of the following primary entities:

- Admin
- Students
- Subjects
- Attendance
- Face Encodings
- Email Logs

---

## 🔄 System Workflow

1. Administrator logs into the system.
2. Student information is registered.
3. Facial images are captured.
4. Face encodings are generated.
5. Administrator starts an attendance session.
6. Webcam captures live faces.
7. Students are identified using facial recognition.
8. Attendance is automatically recorded.
9. Daily reports are generated.
10. Email notifications are sent for absences and low attendance.
11. Students log in to monitor their attendance.

---

## 🔐 Authentication

The application supports **role-based authentication**.

### Administrator

- Username
- Password

### Student

- Roll Number
- Password

Passwords are securely stored using password hashing.

---

## 📈 Future Enhancements

- Mobile application support
- Cloud deployment
- Multi-classroom attendance
- QR code attendance backup
- Face mask detection
- AI-powered attendance analytics
- Multi-factor authentication
- REST API integration

---

## 🚀 Getting Started

### Clone the repository

```bash
git clone https://github.com/yourusername/smart-attendance-system.git
```

### Navigate into the project

```bash
cd smart-attendance-system
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
python app.py
```

---

## 🎯 Project Objectives

- Automate attendance marking
- Prevent proxy attendance
- Improve attendance accuracy
- Reduce manual work
- Provide attendance analytics
- Notify students automatically
- Improve administrative efficiency

---

## 👥 Contributors

- **Abin Gomez**
- **Faisal L**
- **Sachu S Kumar**

---

## 📜 License

This project is developed for educational purposes as part of the **Bachelor of Computer Applications (BCA) Major Project**.

Feel free to use and modify it for learning purposes.

---

⭐ If you found this project useful, consider giving it a star!
