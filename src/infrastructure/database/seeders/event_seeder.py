from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from infrastructure.database.models.user import UserModel
import os
import io
from starlette.datastructures import UploadFile as StarletteUploadFile
from infrastructure.services.image_service import ImageService
from sqlalchemy.orm import selectinload
from infrastructure.database.models.event_organizer import EventOrganizerModel
from infrastructure.database.models.event import EventTypeEnum, EventStatusEnum
from infrastructure.database.models.organization_member import OrganizationMemberModel
from infrastructure.database.models.event import EventModel
import shutil

async def event_seeder(db: AsyncSession):
    try:
        directory_path = "uploads/thumbnails"

        if os.path.exists(directory_path):
            shutil.rmtree(directory_path)
            os.makedirs(directory_path)

        image_service = ImageService(storage_directory=directory_path)

        # Get event organizer
        query = select(UserModel).where(UserModel.role == "EVENT_ORGANIZER").join(EventOrganizerModel, UserModel.user_id == EventOrganizerModel.user_id).options(selectinload(UserModel.event_organizer))
        result = await db.execute(query)
        user = result.scalars().first()
        event_organizer = user.event_organizer

        # Get organization members
        query = select(OrganizationMemberModel).where(OrganizationMemberModel.event_organizer_id == event_organizer.event_organizer_id)
        result = await db.execute(query)
        organization_members = result.scalars().first()

        thumbnail_dir = "src/infrastructure/database/seeders/thumbnail"
        thumbnail_path = os.path.join(thumbnail_dir, os.listdir(thumbnail_dir)[0])

        print("NIH", thumbnail_path)

        with open(thumbnail_path, "rb") as image_file:
            simulated_file = io.BytesIO(image_file.read())
            simulated_file.seek(0)
            upload_file = StarletteUploadFile(filename="thumbnail.jpg", file=simulated_file)

        events = [
                {
                    "event_organizer_id": event_organizer.event_organizer_id,
                    "title": "Tech Summit 2023: Innovating the Future",
                    "address": "123 Main Street",
                    "description": "Join industry leaders and tech enthusiasts to explore cutting-edge innovations shaping the future.",
                    "type": EventTypeEnum.KONVERENSI.value,
                    "status": EventStatusEnum.BUKA.value,
                    "ticket_price": 50000,
                    "ticket_quantity": 200,
                    "start_date": "2023-01-15",
                    "receptionist_1": organization_members.organization_member_id,
                    "receptionist_2": None,
                    "created_at": "2023-01-01T00:00:00",
                    "updated_at": "2023-01-01T00:00:00"
                },
                {
                    "event_organizer_id": event_organizer.event_organizer_id,
                    "title": "Culinary Artistry: The Fusion of Flavors",
                    "address": "45 Culinary Avenue",
                    "description": "Experience a gourmet journey through workshops and tastings with renowned chefs.",
                    "type": EventTypeEnum.WORKSHOP.value,
                    "status": EventStatusEnum.BUKA.value,
                    "ticket_price": 75000,
                    "ticket_quantity": 100,
                    "start_date": "2023-02-10",
                    "receptionist_1": organization_members.organization_member_id,
                    "receptionist_2": None,
                    "created_at": "2023-01-01T00:00:00",
                    "updated_at": "2023-01-01T00:00:00"
                },
                {
                    "event_organizer_id": event_organizer.event_organizer_id,
                    "title": "Mind & Motion: Yoga and Wellness Retreat",
                    "address": "78 Green Valley Road",
                    "description": "Revitalize your mind and body with yoga sessions, mindfulness practices, and nature exploration.",
                    "type": EventTypeEnum.LAINNYA.value,
                    "status": EventStatusEnum.BUKA.value,
                    "ticket_price": 120000,
                    "ticket_quantity": 50,
                    "start_date": "2023-03-01",
                    "receptionist_1": organization_members.organization_member_id,
                    "receptionist_2": None,
                    "created_at": "2023-01-01T00:00:00",
                    "updated_at": "2023-01-01T00:00:00"
                },
                {
                    "event_organizer_id": event_organizer.event_organizer_id,
                    "title": "Future Builders: Coding for Tomorrow",
                    "address": "99 Innovation Drive",
                    "description": "A hands-on coding bootcamp for beginners and professionals to learn the latest in tech development.",
                    "type": EventTypeEnum.WORKSHOP.value,
                    "status": EventStatusEnum.BUKA.value,
                    "ticket_price": 30000,
                    "ticket_quantity": 150,
                    "start_date": "2023-04-05",
                    "receptionist_1": organization_members.organization_member_id,
                    "receptionist_2": None,
                    "created_at": "2023-01-01T00:00:00",
                    "updated_at": "2023-01-01T00:00:00"
                },
                {
                    "event_organizer_id": event_organizer.event_organizer_id,
                    "title": "EcoWorld: Sustainability and Innovation Expo",
                    "address": "21 Green Earth Lane",
                    "description": "Discover groundbreaking eco-friendly solutions and connect with sustainability pioneers.",
                    "type": EventTypeEnum.LAINNYA.value,
                    "status": EventStatusEnum.BERLANGSUNG.value,
                    "ticket_price": 0,
                    "ticket_quantity": 0,
                    "start_date": "2023-05-20",
                    "receptionist_1": organization_members.organization_member_id,
                    "receptionist_2": None,
                    "created_at": "2023-01-01T00:00:00",
                    "updated_at": "2023-01-01T00:00:00"
                },
                {
                    "event_organizer_id": event_organizer.event_organizer_id,
                    "title": "Artistry Unleashed: A Creative Experience",
                    "address": "66 Artistic Boulevard",
                    "description": "Dive into a world of creativity with hands-on art workshops, live demonstrations, and gallery showcases.",
                    "type": EventTypeEnum.FESTIVAL.value,
                    "status": EventStatusEnum.BUKA.value,
                    "ticket_price": 40000,
                    "ticket_quantity": 300,
                    "start_date": "2023-06-15",
                    "receptionist_1": organization_members.organization_member_id,
                    "receptionist_2": None,
                    "created_at": "2023-01-01T00:00:00",
                    "updated_at": "2023-01-01T00:00:00"
                }
            ]

        for event_data in events:
            thumbnail_path = image_service.save_image(image=upload_file, filename=f"{event_data['title'].replace(' ', '_')}_thumbnail.jpg", subdir=event_organizer.organization_name.replace(" ", "_"))
            
            event = EventModel(
                thumbnail_path=thumbnail_path,
                **event_data
            )

            db.add(event)

        await db.commit()
        await db.refresh(events)


    except ValueError as e:
        await db.rollback()
        print(f"Error awdaw events: {e}")

    except Exception as e:
        await db.rollback()
        print(f"Error seeding events: {e}")