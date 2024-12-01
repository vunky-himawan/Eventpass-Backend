from typing import Dict, List
from deepface import DeepFace
import numpy as np
from fastapi import UploadFile
from mtcnn import MTCNN
from PIL import Image
from scipy.spatial.distance import euclidean

class FaceRecognitionService:
    def __init__(self):
        self.model = DeepFace.build_model(model_name='Facenet512')
    
    async def detect_faces(self, image: UploadFile) -> dict:
        try:
            detector = MTCNN()

            image = Image.open(image.file)
        	
            image = image.convert("RGB")

            image_array = np.array(image)

            # Check if the image is empty
            if image_array.size == 0:
                return {
                    "status": "error",
                    "message": "Gambar tidak ditemukan"
                }
            
            # Mengambil data face
            faces = detector.detect_faces(image_array)

            if not faces:
                return {
                    "status": "error",
                    "message": "Tidak ada wajah yang ditemukan"
                }
            
            return {
                "status": "success",
                "message": "Wajah ditemukan",
                "data": {
                    "faces": faces,
                    "original_image": image_array
                }
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Error detecting faces: {e}"
            }
        
    async def extract_face(self, faces: list[dict], image_array: np.ndarray) -> Image:
        try:
            print(f"Faces: {faces}")

            # Cari wajah dengan ukuran bounding box terbesar
            largest_face = max(faces, key=lambda face: face['box'][2] * face['box'][3])  # width * height
            
            # Ekstrak koordinat dari bounding box
            x, y, width, height = largest_face['box']

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
            return None

    async def feature_extraction(self, face_pixels: Image) -> dict:
        try:
            face_pixels = np.array(face_pixels)

            # scale pixel values
            face_pixels = face_pixels.astype('float32')
            
            # standardize pixel values across channels (global)
            mean, std = face_pixels.mean(), face_pixels.std()
            face_pixels = (face_pixels - mean) / std
            
            # transform face into one sample
            samples = np.expand_dims(face_pixels, axis=0)
            
            # make prediction to get embedding
            yhat = self.model.model.predict(samples)

            return {"status": "success", "data": yhat[0]}
        except Exception as e:
            print(f"Error feature extraction: {e}")

    async def predict(self, target_embedding: np.ndarray, val_embeddings: Dict[str, np.ndarray]) -> dict:
        try:
            best_match = None
            best_distance = float('inf')
            confidence = 0.0

            for val_class, val_emb in val_embeddings.items():

                distance = euclidean(target_embedding, val_emb)
                
                if distance < best_distance:
                    best_distance = distance
                    best_match = val_class

            if best_match is not None:
                all_distances = [
                    euclidean(target_embedding, emb) for emb in val_embeddings.values()
                ]
                max_distance = max(all_distances) if all_distances else 1
                confidence = 1 - (best_distance / max_distance)
            else:
                confidence = 0.0

            response = {
                "username": best_match,
                "confidence": confidence,
                "distance": best_distance,
            }

            return response
        
        except ValueError as e:
            print(f"ValueError: {e}")
        except Exception as e:
            print(f"Error predicting: {e}")
    
    async def to_blob(self, face_embedding: np.ndarray) -> bytes:
        return face_embedding.tobytes()
    
    async def from_blob(self, blob: bytes, dtype=np.float32, shape=(128,)) -> np.ndarray:
        return np.frombuffer(blob, dtype=dtype).reshape(shape)