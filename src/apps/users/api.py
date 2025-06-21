import datetime
from fastapi import APIRouter, Depends, HTTPException
from src.auth import create_access_token
from src.apps.users.schemas import UserLoginSchema, UserRegisterSchema, UserResponseSchema
from src.auth import get_current_user
from src.auth import hash_password, verify_password
from src.database import db

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def get_users():
    cursor = db.users.find({})
    users = []
    async for user in cursor:
        user["_id"] = str(user["_id"])
        users.append(user)

    return users


@router.post("/register")
async def register_user(user: UserRegisterSchema):
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_dict = user.model_dump()
    user_dict["hashed_password"] = hash_password(user.password)
    del user_dict["password"]
    user_dict["created_at"] = datetime.datetime.now(datetime.UTC)
    user_dict["is_active"] = True

    result = await db.users.insert_one(user_dict)
    return {"message": f"User {result.inserted_id} registered successfully"}


@router.post("/login")
async def login(form: UserLoginSchema):
    user = await db.users.find_one({"email": form.email})
    if not user or not verify_password(form.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    data = {
        "sub": str(user["_id"]),
        "name": user["name"],
        "email": user["email"]
    }
    token = create_access_token(data)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponseSchema)
async def me(current_user: dict = Depends(get_current_user)):
    data = {
        "id": current_user["_id"],
        "name": current_user["name"],
        "email": current_user["email"],
        "created_at": current_user["created_at"],
        "is_active": current_user["is_active"]
    }
    return data