# 🧠 Usalama Wangu – Backend

## Overview

The **Usalama Wangu Backend** powers all the core functionality of the Usalama Wangu system — a rapid-response safety platform enabling users to send emergency alerts and share real-time location data.
Built using **Django REST Framework**, this backend provides a secure and scalable API consumed by the React Native (Expo) mobile frontend.

---

## ⚙️ Features

- 🚨 **Emergency Alerts** – Receives and processes distress signals from the mobile app.
- 🗺️ **Zone Management** – Handles region and location-based grouping of alerts.
- ☁️ **Cloudinary Integration** – Enables media upload for photos and videos.
- 🔐 **Environment-Based Configuration** – Secure API keys and database credentials.
- 🧩 **Modular Apps** – Independent Django apps (`Alerts`, `Zones`, `api`) for clarity and scalability.

---

## 🧱 Project Structure

```
backend/
│
├── Alerts/ # Manages emergency alert models and logic
├── Zones/ # Handles location and zone operations
├── api/ # REST API endpoints
├── templates/ # Optional HTML templates
├── Usalama_Wangu/ # Project configuration and settings
├── manage.py # Django management utility
├── .env # Environment variables (not committed)
└── .gitignore
```

---

## 🧩 Setup Guide

### 1️⃣ Create and Activate a Virtual Environment

Use either `pip` or `uv`. Example with `pip`:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate     # On Windows
# or
source .venv/bin/activate  # On macOS/Linux
```

### 2️⃣ Install Dependencies

```bash
pip install -r ../requirements.txt
```

### 3️⃣ Set Up Environment Variables

Open `backend/.env` and fill in your credentials:

```env
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=

EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

GROQ_API_KEY=
```

### 4️⃣ Run Database Migrations

```bash
cd backend
python manage.py migrate
```

### 5️⃣ Start the Backend Server

Find your local IP address (e.g., `192.168.5.78`), then run:

```bash
python manage.py runserver 192.168.5.78:4000
```

---

You might need to add your IP address in ALLOWED_HOSTS array in `backend/Usalama_Wangu/settings.py`.
---