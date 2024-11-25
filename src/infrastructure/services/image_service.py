import os
from PIL import Image
from fastapi import UploadFile
from datetime import datetime

class ImageService:
    def __init__(self, storage_directory: str):
        self.storage_directory = storage_directory
        os.makedirs(self.storage_directory, exist_ok=True)

    def save_image(self, image: UploadFile, filename: str, subdir:str=None) -> str:
        # Mengambil ekstensi dari nama file
        file_extension = os.path.splitext(filename)[1]
        if not file_extension:
            raise ValueError("Filename must have an extension")

        # Membaca file gambar menggunakan PIL
        try:
            image_data = Image.open(image.file)  # Membuka file gambar
            filepath = None
            if subdir:
                os.makedirs(os.path.join(self.storage_directory, subdir), exist_ok=True)
            # Menyimpan gambar dengan kualitas tertentu
            if not subdir:
                filepath = os.path.join(self.storage_directory, filename)
            else:
                filepath = os.path.join(self.storage_directory, subdir.replace(" ", "_"), filename)

            image_data.save(filepath, format=image_data.format, quality=85, optimize=True)
            return filepath  # Kembalikan path ke gambar yang disimpan
        except Exception as e:
            # Tangani kesalahan jika ada
            print(f"Error saving image: {e}")
            return None
        
    def save_face_data(self, image: UploadFile, username: str) -> dict:
        try:
            # Membuat direktori untuk penyimpanan gambar sesuai dengan username
            user_directory = os.path.join(self.storage_directory, username)
            os.makedirs(user_directory, exist_ok=True)

            # Menyimpan gambar dengan kualitas tertentu
            current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{current_datetime}_{username}.jpg"

            filepath = os.path.join(user_directory, filename)
            image.save(filepath, format='JPEG', quality=95, optimize=True)
            
            return {
                "status": "success",
                "message": "Gambar berhasil disimpan",
                "data": filepath
            }
        
        except ValueError as e:
            print(f"Error saving face data: {e}")
            raise ValueError("Terjadi kesalahan dalam memproses gambar")
        except Exception as e:
            print(f"Error saving face data: {e}")
            raise Exception("Terjadi kesalahan dalam memproses gambar")
        

    async def delete_face_data(self, username: str) -> dict:
        try:
            path = os.path.join(self.storage_directory, username)
            os.remove(path)
            return {"status": "success", "message": "Gambar berhasil dihapus"}

        except Exception as e:
            raise Exception("Terjadi kesalahan dalam menghapus gambar")