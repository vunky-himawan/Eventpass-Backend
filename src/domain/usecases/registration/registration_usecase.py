from domain.repositories.authentication.authentication_repository import AuthenticationRepository
from infrastructure.services.password_service import PasswordService
from domain.repositories.user.user_repository import UserRepository
from domain.usecases.registration.registration_params import RegistrationParams
from domain.entities.result.result import Failed, Success, Result
from domain.entities.user.user import User
from domain.entities.enum.role import Role
from infrastructure.services.image_service import ImageService
from infrastructure.services.face_recognition_service import FaceRecognitionService

class RegistrationUseCase:
    def __init__(self, password_service: PasswordService, user_repository: UserRepository, authentication_repository: AuthenticationRepository, image_service: ImageService, face_recignition_service: FaceRecognitionService):
        self.password_service = password_service
        self.user_repository = user_repository
        self.authentication_repository = authentication_repository
        self.image_service = image_service
        self.face_recignition_service = face_recignition_service

    async def call(self, params: RegistrationParams) -> Result[User]:
        try:
            # Check if user already exists by username
            user = await self.authentication_repository.get_user_by_username(params.username)

            if user.is_success():
                return Failed(message="Username sudah terdaftar")
            
            # Check if user already exists by email
            user = await self.authentication_repository.get_user_by_email(params.email)

            if user.is_success():
                return Failed(message="Email sudah terdaftar")
            
            # Hash password
            hashed_password = self.password_service.hash_password(params.password)

            # Create user
            new_user = None
            if params.role == Role.RECEPTIONIST.value:
                new_user = await self.user_repository.create_user(
                    username=params.username, 
                    password=hashed_password, 
                    email=params.email, 
                    role=params.role, 
                    details=params.details
                )

            elif params.role == Role.PARTICIPANT.value:
                # Get face photo
                face_photo = await self.face_recignition_service.detect_faces(image=params.face_photo)

                if face_photo.get("status") == "error":
                    return Failed(message=face_photo.get("message"))
                
                
                face_photo = await self.face_recignition_service.extract_face(face=face_photo.get("data").get("face"), 
                                                                            image_array=face_photo.get("data").get("original_image"))
                
                # Save face photo
                face_photo_path = self.image_service.save_face_data(image=face_photo, 
                                                                    username=params.username)
                                
                if face_photo_path.get("status") == "error":
                    return Failed(message=face_photo_path.get("message"))
                
                print("Face photo path: ", face_photo_path)
                
                feature_vector = await self.face_recignition_service.feature_extraction(face_pixels=face_photo)

                feature_vector_blob = await self.face_recignition_service.to_blob(feature_vector.get("data"))

                new_user = await self.user_repository.create_user(username=params.username,
                                                                password=hashed_password, 
                                                                email=params.email, 
                                                                role=params.role,
                                                                feature_vector=feature_vector_blob,
                                                                picture_path=face_photo_path.get("data"),
                                                                details=params.details)

            elif params.role == Role.EVENT_ORGANIZER.value:
                new_user = await self.user_repository.create_user(username=params.username, 
                                                                password=hashed_password, 
                                                                email=params.email, 
                                                                role=params.role, 
                                                                details=params.details)
        
            if new_user.is_success():
                return Success(value=new_user.result_value())
            else:
                return Failed(message=new_user.error_message())
            
        except ValueError as e:
            print("ValueError di REGISTRATION USE CASE: ", e)
            return Failed(message="Terjadi kesalahan dalam proses pendaftaran")
        except Exception as e:
            print("EXCEPTION di REGISTRATION USE CASE: ", e)
            return Failed(message="Terjadi kesalahan dalam proses pendaftaran")
