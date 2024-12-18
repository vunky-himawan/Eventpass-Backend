from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from domain.repositories.user.user_repository import UserRepository
from domain.entities.user.user import User
from infrastructure.database.models.organization_member import OrganizationMemberModel
from infrastructure.database.models.user import UserModel
from domain.entities.result.result import Failed, Success, Result
from domain.entities.participant.participant import Participant
from domain.entities.event_organizer.event_organizer import EventOrganizer
from domain.entities.enum.role import Role
from infrastructure.database.models.participant import ParticipantModel
from infrastructure.database.models.face_photos import FacePhotoModel
from infrastructure.database.models.event_organizer import EventOrganizerModel
from datetime import datetime
from domain.entities.organization_member.organization_member import OrganizationMember

from interface.http.api.schemas.event_organizer.receptionis.main import Receptionist

class UserRepositoryImplementation(UserRepository):
    def __init__(self, db: AsyncSession):
        self._db_session = db

    async def create_user(
            self, 
            username: str, 
            email: str, 
            password: str, 
            role: Role, 
            feature_vector: bytes | None = None, 
            picture_path: str | None = None,
            details: Participant | EventOrganizer | Receptionist  | None = None
        ) -> Result[User]:
        try:
            if not all([username, email, password, role]):
                raise ValueError("Email, username, password, dan role harus diisi")

            try:
                new_user_model = UserModel(
                    username=username,
                    email=email,
                    password=password,
                    role=role
                )
            
            except Exception as e:
                print(e)
                return Failed(message="Terjadi kesalahan")

            self._db_session.add(new_user_model)
            await self._db_session.flush()

            if (role == Role.RECEPTIONIST.value) and (details is not None):
                try:
                    new_receptionist = OrganizationMemberModel(
                        event_organizer_id=details.event_organizer_id,
                        user_id=new_user_model.user_id,
                    )

                    self._db_session.add(new_receptionist)
                    await self._db_session.flush()
                except ValueError as e:
                    await self._db_session.rollback()
                    return Failed(message="Terjadi kesalahan")

            if role == Role.PARTICIPANT.value:
                if details is None:
                    return Failed(message="Participant details are required")

                try:
                    new_participant = ParticipantModel(
                        participant_name=details.participant_name,
                        age=details.age,
                        birth_date=details.birth_date,
                        gender=details.gender.value,
                        user_id=new_user_model.user_id,
                        created_at=datetime.now(),
                        updated_at=datetime.now()
                    )

                    self._db_session.add(new_participant)
                    await self._db_session.flush()

                    if feature_vector:
                        feature = FacePhotoModel(
                            participant_id=new_participant.participant_id,
                            feature_vector=feature_vector,
                            picture_path=picture_path
                        )

                        self._db_session.add(feature)

                except ValueError as e:
                    await self._db_session.rollback()
                    return Failed(message="Terjadi kesalahan")
                except Exception as e:
                    await self._db_session.rollback()
                    return Failed(message="Terjadi kesalahan")

            elif role == Role.EVENT_ORGANIZER.value:

                try:
                    new_event_organizer = EventOrganizerModel(
                        user_id=new_user_model.user_id,
                        organization_name=details.organization_name,
                        address=details.address,
                        phone_number=details.phone_number,
                        email=details.email,
                        description=details.description
                    )

                    self._db_session.add(new_event_organizer)

                except ValueError as e:
                    await self._db_session.rollback()
                    return Failed(message="Terjadi kesalahan")
                except Exception as e:
                    await self._db_session.rollback()
                    return Failed(message="Terjadi kesalahan")

            await self._db_session.commit() 
            await self._db_session.refresh(new_user_model) 
                
            return Success(value=self._model_to_entity(new_user_model))

        except Exception as e:
            await self._db_session.rollback()
            return Failed(message="Terjadi kesalahan")
    
    async def update_user(self, user: User) -> Result[User]:
        try:
            query = select(UserModel).where(UserModel.user_id == user.user_id) 
            result = await self._db_session.execute(query)
            existing_user = result.scalar_one_or_none()

            if existing_user is None:
                return Failed(message="User not found")

            existing_user.username = user.username
            existing_user.refresh_token = user.refresh_token
            existing_user.email = user.email

            await self._db_session.flush()
            await self._db_session.commit()
            await self._db_session.refresh(existing_user)
            
            return Success(value=self._model_to_entity(existing_user))

        except ValueError as e:
            print(e)
            return Failed(message="Terjadi kesalahan")
        except Exception as e:
            print(e)
            return Failed(message="Terjadi kesalahan")

    async def update_user_details(self, user_id: str, details: Participant | EventOrganizer) -> Result[User | Participant | EventOrganizer]:
        # Implement user update logic
        pass
    
    async def delete_user(self, user_id: str) -> Result[bool]:
        # Implement user deletion logic
        pass
    
    async def get_user_details(self, user: User) -> Result[None | Participant | EventOrganizer]:
        try:
            if user.role == Role.PARTICIPANT.value: 
                query = select(UserModel).options(joinedload(UserModel.participant)).where(UserModel.user_id == user.user_id)
                result = await self._db_session.execute(query)
                user = result.scalar_one()

                print(self._model_to_participant(user.participant))

                return Success(value=self._model_to_participant(user.participant))
            elif user.role == Role.EVENT_ORGANIZER.value:
                query = select(UserModel).options(joinedload(UserModel.event_organizer)).where(UserModel.user_id == user.user_id)
                result = await self._db_session.execute(query)
                user = result.scalar_one()
                
                return Success(value=self._model_to_event_organizer(user.event_organizer))

            elif user.role == Role.RECEPTIONIST.value:
                query = select(UserModel).options(joinedload(UserModel.organization_member)).where(UserModel.user_id == user.user_id)
                result = await self._db_session.execute(query)
                user = result.scalar_one()

                return Success(value=self._model_to_organization_member(user.organization_member))
            
            return Success(value=None)

        except ValueError as e:
            print(e)
            return Failed(message="Terjadi kesalahan")
        except Exception as e:
            print(e)
            return Failed(message="Terjadi kesalahan")

    async def upload_profile_photo(self, user_id: str, profile_photo: str) -> Result[bool]:
        # Implement user profile photo upload logic
        pass

    async def get_users(self, skip: int = 0, limit: int = 10) -> Result[list[User | Participant | EventOrganizer]]:
        # Implement user retrieval logic
        pass

    async def get_user_by_user_id(self, user_id: str, with_password: bool | None = None) -> Result[dict]:
        try:
            query = select(UserModel).where(UserModel.user_id == user_id)
            result = await self._db_session.execute(query)
            user = result.scalar_one()

            if user is None:
                return Failed(message="User not found")
            
            return Success(value=user.user_to_dict_with_details(with_password=with_password))

        except ValueError as e:
            return Failed(message="Terjadi kesalahan")
        except Exception as e:
            return Failed(message="Terjadi kesalahan")
        
    async def get_user_by_username(self, username: str) -> Result[dict]:
        try:
            query = select(UserModel).where(UserModel.username == username)
            result = await self._db_session.execute(query)
            user = result.scalar_one()

            if user is None:
                return Failed(message="User not found")
            
            return Success(value=user.user_to_dict_with_details())

        except ValueError as e:
            return Failed(message="Terjadi kesalahan")
        except Exception as e:
            return Failed(message="Terjadi kesalahan")

    async def get_user_by_refresh_token(self, refresh_token: str) -> Result[User]:
        try:
            query = select(UserModel).where(UserModel.refresh_token == refresh_token)
            result = await self._db_session.execute(query)
            user = result.scalar_one()

            if user is None:
                return Failed(message="User not found")
            
            return Success(value=self._model_to_entity(user))

        except ValueError as e:
            return Failed(message="Terjadi kesalahan")
        except Exception as e:
            return Failed(message="Terjadi kesalahan")
        
    async def change_password(self, user_id: str, new_password: str) -> Result[bool]:
        try:
            query = select(UserModel).where(UserModel.user_id == user_id)
            result = await self._db_session.execute(query)
            user = result.scalar_one()

            if user is None:
                return Failed(message="User not found")
            
            user.password = new_password
            await self._db_session.flush()
            await self._db_session.commit()
            await self._db_session.refresh(user)
            
            return Success(value=True)

        except ValueError as e:
            return Failed(message="Terjadi kesalahan")
        except Exception as e:
            return Failed(message="Terjadi kesalahan")
            

    def _model_to_entity(self, model: UserModel) -> User:
        return User(
            user_id=model.user_id,
            username=model.username,
            email=model.email,
            password=model.password,
            role=model.role,
            profile_photo=model.profile_photo_path,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _model_to_participant(self, model: ParticipantModel) -> Participant:
        return Participant(
            participant_name=model.participant_name,
            participant_id=model.participant_id,
            birth_date=model.birth_date,
            age=model.age,
            gender=model.gender.value,
            amount=model.amount,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
    
    def _model_to_event_organizer(self, model: EventOrganizerModel) -> EventOrganizer:
        return EventOrganizer(
            event_organizer_id=model.event_organizer_id,
            organization_name=model.organization_name,
            address=model.address,
            phone_number=model.phone_number,
            email=model.email,
            description=model.description,
            amount=model.amount,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
    
    def _model_to_organization_member(self, model: OrganizationMemberModel) -> OrganizationMember:
        return OrganizationMember(
            organization_member_id=model.organization_member_id,
            user_id=model.user_id,
            event_organizer_id=model.event_organizer_id
        )
    

