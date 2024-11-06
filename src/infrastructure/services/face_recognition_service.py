import cv2
from deepface import DeepFace
import numpy as np

class FaceRecognitionService:
    def get_embedding(self, image_path: str) -> np.ndarray:
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Image not found or unable to read.")

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        result = DeepFace.represent(img_rgb, model_name="Facenet512")
        
        embedding = np.array(result[0]['embedding'])

        return embedding
    
    def to_blob(self, face_embedding: np.ndarray) -> bytes:
        return face_embedding.tobytes()
    
    def from_blob(self, blob: bytes, dtype=np.float32, shape=(128,)) -> np.ndarray:
        return np.frombuffer(blob, dtype=dtype).reshape(shape)