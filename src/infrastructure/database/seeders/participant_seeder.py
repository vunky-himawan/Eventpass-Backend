from sqlalchemy.ext.asyncio import AsyncSession
import os
from passlib.context import CryptContext
from infrastructure.database.models.user import UserModel
from infrastructure.database.models.participant import ParticipantModel
from infrastructure.services.image_service import ImageService
from infrastructure.database.models.face_photos import FacePhotoModel
from infrastructure.services.face_recognition_service import FaceRecognitionService
import io
from starlette.datastructures import UploadFile as StarletteUploadFile
import shutil


async def participant_seeder(db: AsyncSession):
    try:
        directory_path = "uploads/dataset"

        if os.path.exists(directory_path):
            shutil.rmtree(directory_path)
            os.makedirs(directory_path)

        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        face_recognition_service = FaceRecognitionService()
        image_service = ImageService(storage_directory=directory_path)

        image_dir = "src/infrastructure/database/seeders/images"
        folder_names = [folder_name for folder_name in os.listdir(image_dir) if os.path.isdir(os.path.join(image_dir, folder_name))]

        participants = []
        file_paths = []
        features = []

        for folder_name in folder_names: 

            folder_path = os.path.join(image_dir, folder_name)
            image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

            if len(image_files) != 1:
                print(f"Folder '{folder_name}' tidak memiliki tepat satu file gambar. Lewatkan folder ini.")
                continue

            image_path = os.path.join(folder_path, image_files[0])

            with open(image_path, "rb") as image_file:
                simulated_file = io.BytesIO(image_file.read())
                upload_file = StarletteUploadFile(filename=image_files[0], file=simulated_file)

                face_photo = await face_recognition_service.detect_faces(upload_file)

                if face_photo.get("status") == "error":
                    continue

                face_photo = await face_recognition_service.extract_face(faces=face_photo.get("data").get("faces"), image_array=face_photo.get("data").get("original_image"))

                face_photo_path = image_service.save_face_data(image=face_photo, username=folder_name.lower().replace(" ", ""))

                if face_photo_path.get("status") == "error":
                    continue

                feature_vector = await face_recognition_service.feature_extraction(face_pixels=face_photo)

                feature_vector_blob = await face_recognition_service.to_blob(feature_vector.get("data"))

                file_paths.append(face_photo_path.get("data"))
                features.append(feature_vector_blob)

                print("test")

                participants.append({
                    "username": folder_name.lower().replace(" ", ""),
                    "password": pwd_context.hash("12345678"),
                    "email": f"{folder_name.lower().replace(' ', '')}@eventpass.com",
                    'profile_picture': face_photo_path.get("data"),
                    "role": "PARTICIPANT",
                    "details": {
                        "participant_name": folder_name.title(),
                        "age": 20,
                        "gender": "LAKI_LAKI",
                        "birth_date": "2004-01-01",
                    }
                })

        print("INI PARTICIPANT", participants)

        for index, participant in enumerate(participants):
            new_user = UserModel(
                username=participant["username"],
                password=participant["password"],
                profile_photo_path=participant["profile_picture"],
                email=participant["email"],
                role=participant["role"]
            )

            db.add(new_user)
            await db.flush()

            new_participant = ParticipantModel(
                user_id=new_user.user_id,
                participant_name=participant["details"]["participant_name"],
                age=participant["details"]["age"],
                gender=participant["details"]["gender"],
                birth_date=participant["details"]["birth_date"]
            )

            db.add(new_participant)
            await db.flush()

            feature = FacePhotoModel(
                participant_id=new_participant.participant_id,
                feature_vector=features[index],
                picture_path=file_paths[index]
            )

            db.add(feature)
            

        await db.commit()
        await db.refresh(new_user)

    except Exception as e:
        await db.rollback()
        print(f"Error seeding participants: {e}")
