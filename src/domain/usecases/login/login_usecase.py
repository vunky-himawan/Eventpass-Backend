from domain.repositories.user.user_repository import UserRepository
from domain.repositories.authentication.authentication_repository import AuthenticationRepository
from infrastructure.services.jwt_token_service import JWTTokenService
from infrastructure.services.password_service import PasswordService
from domain.usecases.login.login_params import LoginParams
from domain.entities.result.result import Result, Failed, Success
from domain.entities.user.user import User

class LoginUseCase:
    def __init__(self, 
                 user_repository: UserRepository, 
                 authentication_repository: AuthenticationRepository, 
                 jwt_service: JWTTokenService,
                 password_service: PasswordService):
        self.user_repository = user_repository
        self.authentication_repository = authentication_repository
        self.jwt_service = jwt_service
        self.password_service = password_service

    async def call(self, params: LoginParams) -> Result[User]:
        try:
            user = await self.authentication_repository.get_user_by_username(params.username)

            if user.is_success():
                if self.password_service.verify_password(params.password, user.result_value().password):                
                    user = User(
                        user_id=user.result_value().user_id,
                        username=user.result_value().username,
                        email=user.result_value().email,
                        role=user.result_value().role.value,
                        password=user.result_value().password,
                    )

                    details = await self.user_repository.get_user_details(user=user)

                    access_token = self.jwt_service.create_access_token(user=user, details=details.result_value())
                    refresh_token = self.jwt_service.create_refresh_token(user=user, details=details.result_value())

                    # Save refresh token to database
                    user.refresh_token = refresh_token

                    new_updated_user = await self.user_repository.update_user(user)

                    if new_updated_user.is_success():
                        return Success(value={
                            "access_token": access_token,
                            "refresh_token": refresh_token
                        })
                    else:
                        return Failed(message=new_updated_user.error_message())

                else:
                    return Failed(message="Username atau password salah")
            else:
                return Failed(message="Username atau password salah")

        except ValueError as e:
            print("ValueError: ", e)
            return Failed(message=str(e))
        except Exception as e:
            print("Exception: ", e)
            return Failed(message=str(e))
