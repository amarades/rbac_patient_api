from fastapi import FastAPI, Request, HTTPException, Depends
from users import mock_users_db

app = FastAPI()

# Dependency to get current user from header
def get_current_user(request: Request):
    user_id = request.headers.get("X-User-ID")
    if not user_id or user_id not in mock_users_db:
        raise HTTPException(status_code=401, detail="Invalid or missing user ID")
    return mock_users_db[user_id]

@app.get("/whoami")
def who_am_i(current_user: dict = Depends(get_current_user)):
    return {"user": current_user}

# To run the application, use the command:
# uvicorn main:app --reload