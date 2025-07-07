# 🛡️ RBAC API for Patient Data Access

A simple FastAPI backend implementing Role-Based Access Control (RBAC) for patient records.

## 🚀 Features

- Role-checking middleware (`admin`, `clinician`, `guest`)
- Simulated auth via request headers
- Protected routes (e.g. only admin can delete)
- Interactive testing via Swagger UI or Postman
- Modular, scalable backend code

## 📦 Requirements

- Python 3.8+
- FastAPI
- Uvicorn

## ⚙️ Installation

```bash
git clone https://github.com/YOUR_USERNAME/rbac-api.git
cd rbac-api
pip install -r requirements.txt
uvicorn main:app --reload
