import uuid
from faker import Faker
from random import choice

from sqlalchemy.orm import Session
from infrastructure.config.database import init_engine
from infrastructure.services.password_service import PasswordService
from infrastructure.database.models.user import UserModel, add_row
import os

class DataSeeder:
    def __init__(
        self,
    ):
        self.engine = init_engine()
        self.fake = Faker("id_ID")

    def seed_users(self, amount: int = 10):
        for _ in range(amount):
            hashed_password = PasswordService().hash_password('123')
            add_row(
                self.engine, 
                self.fake.user_name(), 
                self.fake.email(), 
                hashed_password, 
                choice(["EVENT_ORGANIZER", "PARTICIPANT", "SUPERADMIN", "RECEPTIONIST"]), 
                "https://www.shutterstock.com/image-vector/people-icon-vector-person-sing-260nw-678922465.jpg"
            )

    def remove_users(self):
        with Session(self.engine) as session:
            session.query(UserModel).delete()
            session.commit()
            session.close()
