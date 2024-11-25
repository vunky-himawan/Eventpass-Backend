from infrastructure.repositories.event.main import EventRepositoryImplementation
from domain.repositories.user.user_repository import UserRepository
from domain.params.attendance.main import AttendanceParams
from domain.entities.result.result import Result, Failed, Success
from infrastructure.services.face_recognition_service import FaceRecognitionService
from infrastructure.services.image_service import ImageService
from domain.repositories.ticket.ticket_repository import TicketRepository
from domain.repositories.face_recognition.face_recognition_repository import FaceRecognitionRepository
import numpy as np

class AttendanceUseCase:
    def __init__(self, 
                 user_repository: UserRepository, 
                 event_repository: EventRepositoryImplementation,
                 face_recognition_service: FaceRecognitionService,
                 face_recognition_repository: FaceRecognitionRepository,
                 ticket_repository: TicketRepository,
                 image_service: ImageService):
        self.user_repository = user_repository
        self.event_repository = event_repository
        self.face_recognition_service = face_recognition_service
        self.ticket_repository = ticket_repository
        self.face_recognition_repository = face_recognition_repository
        self.image_service = image_service

    async def call(self, params: AttendanceParams) -> Result[dict]:
        try:
            event = await self.event_repository.get_event_with_on_going_status_with_receptionist_id(receptionist_id=params.receptionist_id);
        
            tickets = await self.ticket_repository.get_tickets_by_event_id(event_id=event["event_id"])

            transactions = [ticket.transaction for ticket in tickets]

            participants = [transaction.participant for transaction in transactions]

            val_data = {}

            for participant in participants:
                feature_blob = await self.face_recognition_repository.get_face_embedding_by_participant_id(participant_id=participant.participant_id)

                feature_array = await self.face_recognition_service.from_blob(feature_blob["feature_vector"], shape=(512,))

                feature_array = np.squeeze(feature_array)

                if feature_array.ndim != 1:
                    raise ValueError(f"Feature vector for {participant.participant_name} is not 1-D")
                
                result = await self.user_repository.get_user_by_user_id(user_id=participant.user_id)

                user = result.result_value()

                val_data.update({user["username"]: feature_array})

            has_face = await self.face_recognition_service.detect_faces(image=params.photo)

            if has_face["status"] == "error":
                return Failed(message=has_face["message"])
            
            face = has_face["data"]["face"]

            face_image = has_face["data"]["original_image"]

            face_image = await self.face_recognition_service.extract_face(face=face, image_array=face_image)

            face_embedding = await self.face_recognition_service.feature_extraction(face_pixels=face_image)
            target_embedding = np.squeeze(np.array(face_embedding.get("data")))

            result = await self.face_recognition_service.predict(target_embedding=target_embedding, val_embeddings=val_data)

            response = {
                "event_id": event["event_id"],
                "prediction": result
            }

            return Success(value=response)

        except Exception as e:
            print("ERROR DI ATTENDANCE USECASE: ", e)
            return Failed(message=str(e))