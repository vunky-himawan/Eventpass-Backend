import cv2
from deepface import DeepFace
import numpy as np
from fastapi import UploadFile
from mtcnn import MTCNN
from PIL import Image

class FaceRecognitionService:
    def get_embedding(self, image_path: str) -> np.ndarray:
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Image not found or unable to read.")

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        result = DeepFace.represent(img_rgb, model_name="Facenet512")
        
        embedding = np.array(result[0]['embedding'])

        return embedding
    
    def detect_faces(self, image: UploadFile) -> dict:
        try:
            detector = MTCNN()

            image = Image.open(image.file)
            image_array = np.array(image)

            # Check if the image is empty
            if image_array.size == 0:
                return {
                    "status": "error",
                    "message": "Gambar tidak ditemukan"
                }
            
            # Mengambil data face
            faces = detector.detect_faces(image_array)

            if len(faces) == 0:
                return {
                    "status": "error",
                    "message": "Tidak ada wajah yang ditemukan"
                }
            elif len(faces) > 1:
                return {
                    "status": "error",
                    "message": "Terdapat lebih dari satu wajah"
                }
            
            return {
                "status": "success",
                "message": "Wajah ditemukan",
                "data": {
                    "face": faces[0],
                    "original_image": image_array
                }
            }

        except Exception as e:
            print(f"Error detecting faces: {e}")
            return False
        
    def preprocess_image(self, face: np.ndarray, image_array: np.ndarray) -> Image:
        try:
            x, y, width, height = face['box']
            
            # Menambahkan margin 100px di setiap sisi
            margin = 100
            x = max(x - margin, 0)
            y = max(y - margin, 0)
            width += 2 * margin
            height += 2 * margin

            # Pastikan koordinat tidak keluar dari ukuran gambar
            x_end = min(x + width, image_array.shape[1])
            y_end = min(y + height, image_array.shape[0])

            # Crop gambar berdasarkan bounding box dengan margin
            cropped_face = image_array[y:y_end, x:x_end]

            # Konversi kembali ke PIL Image
            cropped_face_image = Image.fromarray(cropped_face)

            # Resize dengan LANCZOS untuk kualitas lebih baik
            resized_image = cropped_face_image.resize((160, 160), Image.LANCZOS)

            return resized_image
        except Exception as e:
            print(f"Error preprocessing image: {e}")
    
    def to_blob(self, face_embedding: np.ndarray) -> bytes:
        return face_embedding.tobytes()
    
    def from_blob(self, blob: bytes, dtype=np.float32, shape=(128,)) -> np.ndarray:
        return np.frombuffer(blob, dtype=dtype).reshape(shape)