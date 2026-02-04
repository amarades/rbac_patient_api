# RBAC API with FastAPI

This project is a **Role-Based Access Control (RBAC) API** built with [FastAPI](https://fastapi.tiangolo.com/), SQLAlchemy, and JWT authentication. It provides endpoints for user authentication, patient management, and note-taking, with role-based permissions for clinicians and admins. A simple frontend is included for demonstration.

---

## Features

- **JWT Authentication**: Secure login and protected endpoints.
- **Role-Based Access**: Only users with the correct role can perform certain actions (e.g., only clinicians can add notes, only admins can delete patients).
- **Patient Management**: Add, list, and delete patients.
- **Notes System**: Clinicians can add notes to patients; all notes are stored in the database.
- **Frontend**: Basic HTML/JS frontend for login, viewing, and managing patients and notes.

---

## Project Structure

```
rbac-api/
│
├── auth.py           # Authentication and role dependencies
├── db.py             # Database connection and session setup
├── main.py           # FastAPI app and API endpoints
├── models.py         # SQLAlchemy models (User, Patient, Note)
├── token_1.py        # JWT creation and decoding
├── create_users.py   # Script to create initial users
├── frontend/
│   └── index.html    # Simple frontend interface
├── .gitignore        # Git ignore file
└── ...
```

---

## How to Run

1. **Install dependencies**  
   ```
   pip install fastapi uvicorn sqlalchemy passlib[bcrypt] python-jose
   ```

2. **Set up the database**  
   - The database is configured in `db.py`. By default, it uses SQLite or PostgreSQL (edit as needed).

3. **Create initial users**  
   - Run `create_users.py` to add admin/clinician users.

4. **Start the server**  
   ```
   uvicorn main:app --reload
   ```

5. **Access the frontend**  
   - Open [http://localhost:8000/frontend/index.html](http://localhost:8000/frontend/index.html) in your browser.

---

## API Endpoints

- `POST /login` — User login, returns JWT token.
- `GET /whoami` — Returns current user info.
- `GET /patients` — List all patients and their notes.
- `POST /patients` — Add a new patient.
- `POST /patients/{patient_id}/notes` — Add a note to a patient (clinician only).
- `DELETE /patients/{patient_id}` — Delete a patient (admin only).

---

## Security Notes

- **Do not commit secrets** (e.g., JWT secret, DB passwords) to GitHub.
- Use a `.env` file or environment variables for sensitive settings.

---

## License

MIT License

---

**This project is a starting point for RBAC-based healthcare or similar applications. Customize and expand it according to your requirements.**