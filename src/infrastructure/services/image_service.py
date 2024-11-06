import os
from PIL import Image
from fastapi import UploadFile
from mtcnn import MTCNN
import numpy as np
from datetime import datetime

class ImageService:
    def __init__(self, storage_directory: str):
        self.storage_directory = storage_directory
        os.makedirs(self.storage_directory, exist_ok=True)

    def save_image(self, image: UploadFile, filename: str) -> str:
        # Mengambil ekstensi dari nama file
        file_extension = os.path.splitext(filename)[1]
        if not file_extension:
            raise ValueError("Filename must have an extension")

        # Membaca file gambar menggunakan PIL
        try:
            image_data = Image.open(image.file)  # Membuka file gambar
            # Menyimpan gambar dengan kualitas tertentu
            filepath = os.path.join(self.storage_directory, filename)
            image_data.save(filepath, format=image_data.format, quality=85, optimize=True)
            return filepath  # Kembalikan path ke gambar yang disimpan
        except Exception as e:
            # Tangani kesalahan jika ada
            print(f"Error saving image: {e}")
            return None
        
    def save_face_data(self, image: UploadFile, username: str) -> str:
        detector = MTCNN()

        try:
            image = Image.open(image.file)
            image_array = np.array(image)

            # Check if the image is empty
            if image_array.size == 0:
                raise ValueError("Gambar tidak ditemukan")
            
            # Mengambil data face
            faces = detector.detect_faces(image_array)

            if len(faces) == 0:
                raise ValueError("Tidak ada wajah yang ditemukan")
            elif len(faces) > 1:
                raise ValueError("Terdapat lebih dari satu wajah")

            face = faces[0]
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
            resized_image = cropped_face_image.resize((224, 224), Image.LANCZOS)

            # Membuat direktori untuk penyimpanan gambar sesuai dengan username
            user_directory = os.path.join(self.storage_directory, username)
            os.makedirs(user_directory, exist_ok=True)

            # Menyimpan gambar dengan kualitas tertentu
            current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{current_datetime}_{username}.jpg"

            filepath = os.path.join(user_directory, filename)
            resized_image.save(filepath, format='JPEG', quality=95, optimize=True)
            
            return filepath
        
        except Exception as e:
            # Log the exception if needed
            print(f"An error occurred: {e}")
            raise ValueError("Terjadi kesalahan saat memproses gambar: " + str(e))