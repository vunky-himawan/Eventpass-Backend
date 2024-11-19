import os
from PIL import Image
from fastapi import UploadFile
from mtcnn import MTCNN
import numpy as np
from datetime import datetime
import uuid
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
from typing import List

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
            raise ValueError("Terjadi kesalahan dalam memproses gambar")
        except Exception as e:
            raise Exception("Terjadi kesalahan dalam memproses gambar")
        

    def augment_face(self, image_path: str, username: str) -> List[str]:
        try:
            output_dir = os.path.join(self.storage_directory, username)
            os.makedirs(output_dir, exist_ok=True)

            img = tf.keras.preprocessing.image.load_img(image_path, target_size=(160, 160))  # Sesuaikan ukuran
            img_array = tf.keras.preprocessing.image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)

            # Data Augmentation
            datagen = ImageDataGenerator(
                rotation_range=40,
                width_shift_range=0.2,
                height_shift_range=0.2,
                shear_range=0.2,
                zoom_range=0.2,
                horizontal_flip=True,
                fill_mode="nearest"
            )

            augmented_paths = []

            # Augmentasi dan tampilkan hasil
            for i, batch in enumerate(datagen.flow(img_array, batch_size=1)):
                augmented_img = batch[0].astype("uint8")
                
                # Simpan hasil dengan nama unik
                unique_name = f"augmented_{uuid.uuid4().hex}.jpg"
                save_path = os.path.join(output_dir, unique_name)
                tf.keras.preprocessing.image.save_img(save_path, augmented_img)

                augmented_paths.append(save_path)
                
                if i == 39:  # Hentikan setelah 40 augmentasi
                    break

            return augmented_paths

        except Exception as e:
            print(f"Error augmenting face: {e}")
