from infrastructure.repositories.event.main import EventRepositoryImplementation
from domain.repositories.user.user_repository import UserRepository
from domain.params.attendance.main import AttendanceParams
from domain.entities.result.result import Result, Failed, Success
from infrastructure.services.face_recognition_service import FaceRecognitionService
from infrastructure.services.image_service import ImageService
from domain.repositories.ticket.ticket_repository import TicketRepository
from domain.repositories.face_recognition.face_recognition_repository import FaceRecognitionRepository
from domain.repositories.organization_member.organization_member_repository import OrganizationMemberRepository
import numpy as np

class AttendanceUseCase:
    def __init__(self, 
                 user_repository: UserRepository, 
                 event_repository: EventRepositoryImplementation,
                 face_recognition_service: FaceRecognitionService,
                 face_recognition_repository: FaceRecognitionRepository,
                 organization_member_repository: OrganizationMemberRepository,
                 ticket_repository: TicketRepository,
                 image_service: ImageService):
        self.user_repository = user_repository
        self.event_repository = event_repository
        self.face_recognition_service = face_recognition_service
        self.organization_member_repository = organization_member_repository
        self.ticket_repository = ticket_repository
        self.face_recognition_repository = face_recognition_repository
        self.image_service = image_service

    async def call(self, params: AttendanceParams) -> Result[dict]:
        try:
            # Mengecek apakah ada face di gambar yang dikirim
            has_face = await self.face_recognition_service.detect_faces(image=params.photo)

            if has_face["status"] == "error":
                return Failed(message=has_face["message"])
            
            # Mendapatkan face dari gambar yang dikirim
            faces = has_face["data"]["faces"]

            # Mendapatkan gambar yang dikirim yang sudah diproses menjadi array
            face_image = has_face["data"]["original_image"]

            # Melakukan crop pada wajah yang dikirim
            face_image = await self.face_recognition_service.extract_face(faces=faces, image_array=face_image)

            # Mendapatkan feature embedding dari wajah yang dikirim
            face_embedding = await self.face_recognition_service.feature_extraction(face_pixels=face_image)
            target_embedding = np.squeeze(np.array(face_embedding.get("data")))
        
            # Mendapatkan tickets yang ada di event
            tickets = await self.ticket_repository.get_tickets_by_event_id(event_id=params.event_id)

            # Mendapatkan event yang sedang berlangsung
            event = await self.event_repository.get_event(event_id=params.event_id)
            event_dict = event.to_dict()

            # Mendapatkan transaksi yang ada di tickets
            transactions = [ticket.transaction for ticket in tickets]
            participants = [transaction.participant for transaction in transactions]

            # Digunakan untuk menyimpan data yang dihasilkan dari proses pengamatan
            val_data = {}

            # Mengambil data face embedding dari setiap participant
            for participant in participants:
                feature_blob = await self.face_recognition_repository.get_face_embedding_by_participant_id(participant_id=participant.participant_id)
                
                # Mengubah tipe data dari blob ke array
                feature_array = await self.face_recognition_service.from_blob(feature_blob["feature_vector"], shape=(512,))
                feature_array = np.squeeze(feature_array)

                if feature_array.ndim != 1:
                    raise ValueError(f"Feature vector for {participant.participant_name} is not 1-D")
                
                result = await self.user_repository.get_user_by_user_id(user_id=participant.user_id)

                user = result.result_value()

                val_data.update({user["username"]: feature_array})

            # Melakukan predict
            result = await self.face_recognition_service.predict(target_embedding=target_embedding, val_embeddings=val_data)

            user_result = await self.user_repository.get_user_by_username(username=result['username'])

            if user_result.is_failed():
                return Failed(message=user_result.error_message())

            user = user_result.result_value()

            response = {
                "event_id": event_dict["event_id"],
                "prediction": result,
                "user": user
            }

            return Success(value=response)

        except ValueError as e:
            return Failed(message=str(e))
        except Exception as e:
            return Failed(message=str(e))