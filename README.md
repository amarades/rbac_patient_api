# 🛡️ RBAC API for Patient Data Access

A simple FastAPI backend + HTML/JS frontend implementing **Role-Based Access Control (RBAC)** to securely view, add, and delete patient records.

---

## 🚀 Features

### ✅ Backend (FastAPI)
- Role-checking middleware (`admin`, `clinician`, `guest`)
- Simulated authentication using custom headers (`X-User-ID`)
- Protected routes:
  - Only **admin** can delete patients
  - **Clinicians** can add notes or patients
  - **Guests** can only view
- Modular and scalable architecture
- Swagger docs available at [`/docs`](http://127.0.0.1:8000/docs)

### 🎨 Frontend (HTML + JS)
- Patient list view
- Add/Delete buttons (role-based)
- Dynamic dropdown to simulate user role switch
- Responsive UI with styling
- CORS enabled for smooth backend communication

---

## 📦 Requirements

- Python 3.8+
- `fastapi`
- `uvicorn`
- `http-server` (for serving frontend locally, optional)

Install dependencies:
```bash
pip install fastapi uvicorn
```

---

## ⚙️ Installation & Running

### 1️⃣ Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/rbac-api.git
cd rbac-api
```

### 2️⃣ Run the backend (FastAPI)
```bash
uvicorn main:app --reload
```

- FastAPI will run at: `http://127.0.0.1:8000`
- API docs: `http://127.0.0.1:8000/docs`

### 3️⃣ Run the frontend (optional)
From inside the `frontend` directory:
```bash
cd frontend
npx http-server .
```

- Open: `http://127.0.0.1:5500` (or the port shown in terminal)

---

## 🔑 Simulated Users

Use the dropdown to simulate different roles:
- **Admin Alice** – Can add/delete/view patients
- **Clinician Bob** – Can add/view patients
- **Guest Gina** – Can only view

Header-based role simulation:
```http
X-User-ID: admin  → Admin Alice
X-User-ID: clinician → Clinician Bob
X-User-ID: guest  → Guest Gina
```

---

## 📁 Project Structure

```
rbac-api/
│
├── main.py             # FastAPI app
├── rbac.py             # Role-checking logic
├── users.py            # Mock user database
├── requirements.txt
│
├── frontend/           # HTML + JS UI
│   ├── index.html
│   └── styles.css
```

---

## 💡 Example Endpoints

| Endpoint | Method | Role |
|----------|--------|------|
| `/whoami` | GET | All |
| `/patients` | GET | All |
| `/patients` | POST | Clinician, Admin |
| `/patients/{id}` | DELETE | Admin |

---

## 📝 Notes

- This project uses **mock data only**; no real DB.
- Can be extended with real auth (JWT) and DB (Postgres, etc.)
- You can test using Postman or Swagger.