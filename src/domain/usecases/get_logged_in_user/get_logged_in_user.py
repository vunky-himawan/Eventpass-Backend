from domain.repositories.authentication.authentication_repository import AuthenticationRepository
from domain.entities.result.result import Result, Failed, Success
from infrastructure.services.jwt_token_service import JWTTokenService

class GetLoggedInUserUseCase:
    def __init__(self, authentication_repository: AuthenticationRepository, jwt_service: JWTTokenService):
        self.authentication_repository = authentication_repository
        self.jwt_service = jwt_service

    async def call(self, token: str) -> Result[dict]:
        try:
            verify_token = self.jwt_service.verify_token(token)

            if not verify_token:
                return Failed(message="Access token tidak valid")

            result = await self.authentication_repository.get_logged_in_user(user_id=verify_token["sub"])

            if result.is_failed():
                return Failed(message="User tidak ditemukan")
            
            return Success(value=result.result_value())
        except ValueError as e:
            return Failed(message=str(e))
        except Exception as e:
            return Failed(message=str(e))