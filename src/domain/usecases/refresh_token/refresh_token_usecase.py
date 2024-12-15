from domain.repositories.user.user_repository import UserRepository
from domain.repositories.authentication.authentication_repository import AuthenticationRepository
from domain.entities.result.result import Result, Failed, Success
from infrastructure.services.jwt_token_service import JWTTokenService
from domain.entities.user.user import User

class RefreshTokenUseCase:
    def __init__(self, 
                 user_repository: UserRepository, 
                 authentication_repository: AuthenticationRepository,
                 jwt_service: JWTTokenService):
        self.user_repository = user_repository
        self.authentication_repository = authentication_repository
        self.jwt_service = jwt_service

    async def call(self, refresh_token: str) -> Result[dict]:
        try:
            verify_token = self.jwt_service.verify_refresh_token(refresh_token)

            if not verify_token:
                return Failed(message="Access token tidak valid")
            
            result = await self.user_repository.get_user_by_refresh_token(refresh_token=refresh_token)

            if result.is_failed():
                return Failed(message="Refresh token tidak valid")
            
            user = User(
                user_id=result.result_value().user_id,
                username=result.result_value().username,
                email=result.result_value().email,
                password=result.result_value().password,
                role=result.result_value().role,
                profile_photo=result.result_value().profile_photo,
                created_at=result.result_value().created_at,
                updated_at=result.result_value().updated_at
            )

            event_id = verify_token["sub"]["event_id"]

            details = await self.user_repository.get_user_details(user=user)

            new_access_token = self.jwt_service.create_access_token(user=user, event_id=event_id, details=details)
            new_refresh_token = self.jwt_service.create_refresh_token(user=user, event_id=event_id, details=details)
            
            user.refresh_token = new_refresh_token

            new_updated_user = await self.user_repository.update_user(user)

            if new_updated_user.is_failed():
                return Failed(message="Refresh token tidak valid")

            return Success(value={
                "access_token": new_access_token,
                "refresh_token": new_refresh_token
            })
        except ValueError as e:
            return Failed(message=str(e))
        except Exception as e:
            return Failed(message=str(e))