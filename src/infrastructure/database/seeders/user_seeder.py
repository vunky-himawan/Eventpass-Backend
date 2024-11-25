from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.models.user import UserModel
from infrastructure.database.models.event_organizer import EventOrganizerModel
from passlib.context import CryptContext
import os


async def seed_user(db: AsyncSession):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    users = [
        {
            "username": "superadmin",
            "password": pwd_context.hash("12345678"),
            "email": "superadmin@eventpass.com",
            "role": "SUPERADMIN",
        },
        {
            "username": "receptionist",
            "password": pwd_context.hash("12345678"),
            "email": "receptionist@eventpass.com",
            "role": "RECEPTIONIST",
        },
        {
            "username": "eventorganizer",
            "password": pwd_context.hash("12345678"),
            "email": "eventorganizer@eventpass.com",
            "role": "EVENT_ORGANIZER",
            "details": {
                "organization_name": "Event Organizer",
                "address": "123 Main Street",
                "phone_number": "123-456-7890",
                "email": "eventorganizer@eventpass.com",
                "description": "description"
            }
        },
    ]    

    for user in users: 

        new_user = UserModel(
            username=user["username"], 
            password=user["password"], 
            email=user["email"], 
            role=user["role"]
        )

        db.add(new_user)
        await db.flush()
        
        # Check if the role is 'EVENT_ORGANIZER' and add related details
        if user.get("role") == "EVENT_ORGANIZER":
            details = user["details"]  # Correctly access the details field
            
            new_event_organizer = EventOrganizerModel(
                user_id=new_user.user_id,  # Assuming user_id is a field in UserModel
                organization_name=details["organization_name"],
                address=details["address"],
                phone_number=details["phone_number"],
                email=details["email"],
                description=details["description"]
            )

            db.add(new_event_organizer)
        
        else:
            db.add(new_user)

    await db.commit()
    await db.refresh(new_user)
