# IPO Web App – Internship Project at Bluestock Fintech

This is a basic IPO Web Application developed as part of my internship at Bluestock Fintech. The app provides IPO-related information to the public, including upcoming, ongoing, and listed IPOs. It also includes a secure REST API, a user-friendly frontend using Bootstrap, and an admin panel for managing IPO entries.

The goal of this project was to learn full-stack web development using Django and Django REST Framework, along with Git, GitHub, and JWT authentication for APIs.

---

## 🔧 Features

### 👥 Public User Interface:
- IPO listings page with filters for status (upcoming, ongoing, listed)
- IPO detail page with:
  - Company name & logo
  - Price band
  - Opening/closing dates
  - Listing date & status
  - Issue size, issue type
  - Listing gain %, current return
  - Downloadable RHP and DRHP PDFs

### 🔐 Admin Panel:
- Login-protected admin dashboard (Django)
- Ability to add, edit, and delete IPO entries
- Upload company logos and PDF documents

### 🔐 REST API (JWT-Protected):
- /api/ipo/ → List all IPOs (secured)
- /api/ipo/<id>/ → Get details of a single IPO (secured)
- Token authentication using *SimpleJWT*
- API tested using *Postman*

---

## 🧑‍💻 Tech Stack

- Python 3.12.3  
- Django 5.0.6  
- Django REST Framework 3.15.1  
- PostgreSQL (can use SQLite for dev)  
- HTML, CSS, JavaScript (Plain)  
- Bootstrap 5 (via CDN)  
- Postman (API Testing)  
- Git & GitHub (Version Control)  
- VS Code (IDE)

---

## 🚀 Setup Instructions (Local Development)

### 1. Clone the repository

```bash
git clone https://github.com/manojcheerala/ipo-web-app.git
cd ipo-web-app