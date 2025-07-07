# rbac.py

from fastapi import HTTPException, Depends
from users import mock_users_db
from fastapi import Request

# Same as before – reuse auth dependency
def get_current_user(request: Request):
    user_id = request.headers.get("X-User-ID")
    if not user_id or user_id not in mock_users_db:
        raise HTTPException(status_code=401, detail="Invalid or missing user ID")
    return mock_users_db[user_id]

# Role-checking dependency
def require_role(allowed_roles: list):
    def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user["role"] not in allowed_roles:
            raise HTTPException(status_code=403, detail="You are not authorized to access this resource.")
        return current_user
    return role_checker
