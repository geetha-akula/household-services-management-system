# Household Services Management System

A full-stack web application built using Flask, Vue.js, SQLite, and JWT Authentication for managing household services. The platform connects customers, service professionals, and administrators through a role-based service management system.

## Project Overview

The Household Services Management System enables users to browse and request household services, allows professionals to manage assigned service requests, and provides administrators with tools to manage users, services, and platform operations.

This project was developed as part of the Modern Application Development II course and demonstrates full-stack application development using a REST API architecture.

---

## Features

### User Features

* User Registration and Login
* JWT-based Authentication
* Browse Available Services
* Book Service Requests
* Track Service Status
* Submit Feedback and Ratings
* Manage User Profile

### Professional Features

* Professional Registration
* View Assigned Service Requests
* Accept or Reject Requests
* Update Service Status
* Manage Professional Profile

### Admin Features

* Manage Services
* Manage Users
* Manage Professionals
* Monitor Platform Activity
* View Administrative Dashboard
* Access Platform Statistics

---

## Technology Stack

### Backend

* Python
* Flask
* Flask RESTful
* Flask SQLAlchemy
* Flask JWT Extended
* Flask CORS
* Flask Caching
* SQLite

### Frontend

* Vue.js
* Vue Router
* Vuex
* Axios

### Tools

* Git
* GitHub
* VS Code

---

## Architecture

```text
Vue.js Frontend
       │
       ▼
REST APIs
       │
       ▼
Flask Backend
       │
       ▼
SQLite Database
```

---

## Project Structure

```text
household-services-management-system
│
├── backend
│   ├── app.py
│   ├── model.py
│   ├── requirements.txt
│   └── Management
│
├── frontend
│   ├── src
│   ├── public
│   ├── package.json
│   └── package-lock.json
│
├── docs
│   └── project_report.pdf
│
├── README.md
└── .gitignore
```

---

## Installation and Setup

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend Setup

```bash
cd frontend
npm install
npm run serve
```

---

## Key Concepts Implemented

* REST API Development
* JWT Authentication
* Role-Based Access Control
* Database Design and Normalization
* CRUD Operations
* Client-Server Architecture
* Frontend–Backend Integration
* State Management using Vuex

---

## Learning Outcomes

* Full-Stack Web Development
* Authentication and Authorization
* API Design and Integration
* Relational Database Design
* Frontend and Backend Collaboration

---

## Screenshots

### Login Page

(Add Screenshot Here)

### User Dashboard

(Add Screenshot Here)

### Professional Dashboard

(Add Screenshot Here)

### Admin Dashboard

(Add Screenshot Here)

---

## Project Report

The detailed project report is available in the `docs` directory.

---

## Future Enhancements

* Email Notifications
* Payment Gateway Integration
* Service Recommendation System
* Real-Time Notifications
* Cloud Deployment
* Advanced Analytics Dashboard

---

## License

This project is licensed under the MIT License.
