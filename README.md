# Usalama Wangu

## 🌍 Overview

**Usalama Wangu** makes it extremely fast and reliable for anyone to request help and share context with one tap.

It is built using **React Native (Expo)** for the frontend and **Django REST Framework (DRF)** for the backend — combining speed, scalability, and reliability for real-time emergency response.

---

## 🚀 Features

- 🆘 One-tap emergency alert system  
- 📍 Real-time location and zone mapping  
- 🔄 Context sharing with backend integration  
- ☁️ Cloudinary and Azure-powered media storage
- 🧩 Modular architecture for easy maintenance

---

## 🧱 Project Structure

```
Usalama-Wangu/
│
├── backend/                      # Django REST Framework backend
│   ├── Alerts/                   # Emergency alert app
│   ├── Zones/                    # Zone and location management
│   ├── api/                      # API endpoints
│   ├── templates/                # HTML templates (if any)
│   ├── Usalama_Wangu/            # Project settings
│   ├── manage.py                 # Django management script
│   └── .env                      # Backend environment variables
│
├── expo-maps/                    # React Native (Expo) frontend
│   ├── app/                      # Main app logic
│   │   ├── components/           # Reusable UI components
│   │   ├── emergencyButtonScreen/
│   │   │   └── hooks/
│   │   │       ├── useEmergencyAlert.ts  # Sends help requests to backend
│   │   │       ├── useLocation.ts
│   │   │       └── ...
│   │   └── index.tsx             # Entry point for the app
│   ├── assets/                   # Images, icons, etc.
│   ├── package.json              # Frontend dependencies
│   ├── app.json                  # Expo configuration
│   └── README.md
│
├── .venv/                        # Python virtual environment
├── requirements.txt              # Backend dependencies
├── .env.example                  # Example environment variables
├── pyproject.toml                # (Optional) if using uv
└── README.md                     # Project documentation
```

---

## ⚙️ Setup Guide

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/<your-username>/Usalama-Wangu.git
cd Usalama-Wangu
```

---

### 2️⃣ Backend Setup (Django REST Framework)

#### Create a Virtual Environment

You can use either **pip** or **uv**. Example using pip:

```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
# or
source .venv/bin/activate  # On macOS/Linux
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Set Up Environment Variables

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

#### Run Database Migrations

```bash
cd backend
python manage.py migrate
```

#### Start the Backend Server

Find your local IP address (e.g., `192.168.5.78`), then run:

```bash
python manage.py runserver 192.168.5.78:4000
```

---

You might need to add your IP address in ALLOWED_HOSTS array in `backend/Usalama_Wangu/settings.py`.

### 3️⃣ Frontend Setup (React Native + Expo)

#### Install Dependencies

```bash
cd ../expo-maps
npm install
# or
npm i
```

---

### 4️⃣ Update API Endpoints

You must update your **local IP address** in the following files whenever it changes:

#### In `app/emergencyButtonScreen/hooks/useEmergencyAlert.ts`
```typescript
const response = await fetch("http://192.168.5.78:4000/api/alert/", {
  method: "POST",
  body: formData,
});
```

#### In `app/index.tsx`
```typescript
const response = await fetch("http://192.168.5.78:4000/api/zones");
```

> Replace `192.168.5.78` with your **current machine’s IP address** each time you start development.

---

### 5️⃣ Run the Frontend

Start Expo:

```bash
npx expo start
```

This opens the **Expo Developer Tools** in your browser and displays a QR code.

Scan the QR code using the **Expo Go** app:

- [Play Store (Android)](https://play.google.com/store/apps/details?id=host.exp.exponent)
- [App Store (iOS)](https://apps.apple.com/app/expo-go/id982107779)

---

## 💡 Development Tips

- Always run both backend (`runserver`) and frontend (`expo start`) on the **same Wi-Fi network**.
- If the frontend cannot reach the backend:
  - Check that your IP address hasn’t changed.
  - Ensure both devices (computer and phone) are on the same network.
  - Allow incoming connections on **port 4000** via your firewall.

---

## 📜 License

This project is open source and available under the **MIT License**.

---

## ✨ Summary

**Usalama Wangu** empowers users to request help instantly and share their real-time location seamlessly through a reliable, mobile-first experience.

Built with **modern, scalable technologies** — **React Native (Expo)** for a fast, intuitive UI and **Django REST Framework** for a robust, secure backend API.

---
