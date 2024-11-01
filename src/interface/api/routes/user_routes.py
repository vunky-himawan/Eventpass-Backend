from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
from ....infrastructure.config import get_db
from ....infrastructure.repositories.user_repository import UserRepository
from ...schemas.user import UserResponse
from fastapi.staticfiles import StaticFiles
import os

router = APIRouter()

# Mount static files for serving profile photos
UPLOAD_DIR = os.getenv('UPLOAD_DIR', 'uploads')
router.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

@router.post("/users/", response_model=UserResponse)
async def create_user(
    username: str = Form(...),
    email: str = Form(...),
    profile_photo: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):
    repository = UserRepository(db)
    user = await repository.create_user(username, email, profile_photo)
    return user

@router.get("/users/", response_model=List[UserResponse])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repository = UserRepository(db)
    users = await repository.get_users(skip=skip, limit=limit)
    return users

@router.get("/users/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    repository = UserRepository(db)
    user = await repository.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    username: str | None = Form(None),
    email: str | None = Form(None),
    profile_photo: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):
    repository = UserRepository(db)
    user = await repository.update_user(user_id, username, email, profile_photo)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    repository = UserRepository(db)
    success = await repository.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}