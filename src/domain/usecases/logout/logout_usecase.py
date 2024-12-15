from domain.repositories.user.user_repository import UserRepository
from domain.entities.result.result import Result, Failed, Success
from infrastructure.services.jwt_token_service import JWTTokenService
from domain.entities.user.user import User

class LogoutUseCase:
    def __init__(self,
                 user_repository: UserRepository,
                 jwt_service: JWTTokenService,):
        self.jwt_service = jwt_service
        self.user_repository = user_repository

    async def call(self, token: str) -> Result[bool]:
        try:
            verify_token = self.jwt_service.verify_token(token=token)

            if not verify_token:
                return Failed(message="Token tidak valid")

            result = await self.user_repository.get_user_by_user_id(user_id=verify_token["sub"], with_password=True)

            if result.is_failed():
                return Failed(message="User tidak valid")
            
            user_result_data = result.result_value()
            
            user = User(
                user_id=user_result_data["user_id"],
                username=user_result_data["username"],
                email=user_result_data["email"],
                password=user_result_data["password"],
                role=user_result_data["role"],
                refresh_token=None,
                profile_photo=user_result_data["profile_photo"],
                created_at=user_result_data["created_at"],
                updated_at=user_result_data["updated_at"]
            )

            updated_user = await self.user_repository.update_user(user)

            if updated_user.is_failed():
                return Failed(message="Refresh token tidak valid")
            
            return Success(value=True)

        except ValueError as e:
            print(e)
            return Failed(message=str(e))
        except Exception as e:
            print(e)
            return Failed(message=str(e))