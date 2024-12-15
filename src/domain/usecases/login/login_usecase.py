from domain.repositories.user.user_repository import UserRepository
from domain.repositories.authentication.authentication_repository import AuthenticationRepository
from infrastructure.services.jwt_token_service import JWTTokenService
from infrastructure.services.password_service import PasswordService
from domain.repositories.organization_member.organization_member_repository import OrganizationMemberRepository
from domain.repositories.event.main import EventRepository
from domain.usecases.login.login_params import LoginParams
from domain.entities.result.result import Result, Failed, Success
from domain.entities.user.user import User
from domain.entities.enum.role import Role

class LoginUseCase:
    def __init__(self, 
                 user_repository: UserRepository, 
                 authentication_repository: AuthenticationRepository, 
                 organization_member_repository: OrganizationMemberRepository,
                 event_repository: EventRepository,
                 jwt_service: JWTTokenService,
                 password_service: PasswordService):
        self.user_repository = user_repository
        self.authentication_repository = authentication_repository
        self.event_repository = event_repository
        self.organization_member_repository = organization_member_repository
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
                        profile_photo=user.result_value().profile_photo,
                        role=user.result_value().role.value,
                        password=user.result_value().password,
                    )

                    event_id = None
                    if user.role == Role.RECEPTIONIST.value:
                        organization_member = await self.organization_member_repository.get_organization_member_by_user_id(user_id=user.user_id)

                        event = await self.event_repository.get_event_with_on_going_status_with_receptionist_id(organization_member['organization_member_id'])

                        event_id = event['event_id']

                    access_token = self.jwt_service.create_access_token(user=user, event_id=event_id)
                    refresh_token = self.jwt_service.create_refresh_token(user=user, event_id=event_id)

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
            return Failed(message=str(e))
        except Exception as e:
            return Failed(message=str(e))
