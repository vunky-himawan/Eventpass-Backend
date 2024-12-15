from domain.repositories.user.user_repository import UserRepository
from infrastructure.services.password_service import PasswordService
from domain.entities.result.result import Result, Success, Failed
from infrastructure.services.jwt_token_service import JWTTokenService

class ChangePasswordUseCase:
    def __init__(self, user_repository: UserRepository, password_service: PasswordService, jwt_service: JWTTokenService):
        self.user_repository = user_repository
        self.jwt_service = jwt_service
        self.password_service = password_service

    async def call(self, token: str, old_password: str, new_password: str) -> Result[bool]:
        try:
            verify_token = self.jwt_service.verify_token(token)

            if verify_token is None:
                return Failed(message="Token tidak valid")
            
            user_id = verify_token['sub']

            result = await self.user_repository.get_user_by_user_id(user_id=user_id, with_password=True)

            if result.is_failed():
                return Failed(message=result.message)
            
            user = result.result_value()
            
            if not self.password_service.verify_password(old_password, user['password']):
                return Failed(message="Password tidak valid")
            
            hashed_password = self.password_service.hash_password(new_password)

            updated_password = await self.user_repository.change_password(user_id=user_id, new_password=hashed_password)

            if updated_password.is_failed():
                return Failed(message=updated_password.message)
            
            return Success(value=True)

        except ValueError as e:
            return Failed(message="Terjadi kesalahan")
        except Exception as e:
            return Failed(message="Terjadi kesalahan")