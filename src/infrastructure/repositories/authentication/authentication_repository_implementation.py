from domain.repositories.authentication.authentication_repository import AuthenticationRepository
from sqlalchemy.ext.asyncio import AsyncSession
from domain.entities.result.result import Result, Failed, Success
from domain.entities.user.user import User
from infrastructure.database.models.user import UserModel
from sqlalchemy.future import select

class AuthenticationRepositoryImplementation(AuthenticationRepository):
    def __init__(self, db: AsyncSession):
        self._db_session = db

    async def get_user_by_username(self, username: str) -> Result[User]:
        try:
            query = select(UserModel).where(UserModel.username == username)
            result = await self._db_session.execute(query)
            user = result.scalar_one_or_none()

            print("awdawdaw")
            print(user)

            if user is None:
                return Failed(message="Pengguna tidak ditemukan")
            
            print("Nih user")
            print(user)
            
            return Success(value=self._model_to_entity(user))

        except ValueError as e:
            print(e)
            return Failed(message=str(e))
        except Exception as e:
            print(e)
            return Failed(message=str(e))

    async def get_user_by_email(self, email: str) -> Result[User]:
        try:
            query = select(UserModel).where(UserModel.email == email)
            result = await self._db_session.execute(query)
            user = result.scalar_one_or_none()

            if user is None:
                return Failed(message="User not found")
            
            return Success(value=self._model_to_entity(user))
        
        except Exception as e:
            return Failed(message=str(e))

    async def update_user_password(self, user_id: str, new_password: str, old_password: str) -> Result[bool]:
        pass

    def _model_to_entity(self, user_model: UserModel) -> User:
        return User(user_id=user_model.user_id,
                    username=user_model.username,
                    role=user_model.role,
                    email=user_model.email,
                    password=user_model.password,
                    profile_photo=user_model.profile_photo_path,
                    created_at=user_model.created_at,
                    updated_at=user_model.updated_at)
