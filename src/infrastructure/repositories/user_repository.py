from sqlalchemy.orm import Session
from ..database.models.user import UserModel
from ...domain.entities.user.user import User
from fastapi import UploadFile
import os
from PIL import Image
import uuid
from datetime import datetime

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    async def create_user(self, username: str, email: str, profile_photo: UploadFile | None = None) -> User:
        # Handle profile photo upload
        photo_path = None
        if profile_photo:
            photo_path = await self._save_profile_photo(profile_photo)

        db_user = UserModel(
            username=username,
            email=email,
            profile_photo=photo_path
        )
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        
        return self._model_to_entity(db_user)

    async def get_user(self, user_id: int) -> User | None:
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if db_user is None:
            return None
        return self._model_to_entity(db_user)

    async def get_users(self, skip: int = 0, limit: int = 100):
        users = self.db.query(UserModel).offset(skip).limit(limit).all()
        return [self._model_to_entity(user) for user in users]

    async def update_user(self, user_id: int, username: str | None = None, 
                         email: str | None = None, profile_photo: UploadFile | None = None) -> User | None:
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if db_user is None:
            return None

        if username:
            db_user.username = username
        if email:
            db_user.email = email
        if profile_photo:
            # Delete old photo if exists
            if db_user.profile_photo:
                self._delete_profile_photo(db_user.profile_photo)
            # Save new photo
            db_user.profile_photo = await self._save_profile_photo(profile_photo)

        db_user.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_user)
        
        return self._model_to_entity(db_user)

    async def delete_user(self, user_id: int) -> bool:
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if db_user is None:
            return False

        # Delete profile photo if exists
        if db_user.profile_photo:
            self._delete_profile_photo(db_user.profile_photo)

        self.db.delete(db_user)
        self.db.commit()
        return True

    async def _save_profile_photo(self, photo: UploadFile) -> str:
        UPLOAD_DIR = os.getenv('UPLOAD_DIR', 'uploads')
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        # Generate unique filename
        ext = os.path.splitext(photo.filename)[1]
        filename = f"{uuid.uuid4()}{ext}"
        filepath = os.path.join(UPLOAD_DIR, filename)

        # Process and save image
        image = Image.open(photo.file)
        # Resize image to maximum dimensions while maintaining aspect ratio
        MAX_SIZE = (800, 800)
        image.thumbnail(MAX_SIZE, Image.Resampling.LANCZOS)
        image.save(filepath, quality=85, optimize=True)

        return filename

    def _delete_profile_photo(self, filename: str):
        if not filename:
            return
        
        filepath = os.path.join(os.getenv('UPLOAD_DIR', 'uploads'), filename)
        if os.path.exists(filepath):
            os.remove(filepath)

    def _model_to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            username=model.username,
            email=model.email,
            profile_photo=model.profile_photo,
            created_at=model.created_at,
            updated_at=model.updated_at
        )