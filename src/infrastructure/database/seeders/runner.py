import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession

project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

load_dotenv()

from infrastructure.database.seeders.user_seeder import seed_user
from infrastructure.database.seeders.participant_seeder import participant_seeder
from infrastructure.database.seeders.event_seeder import event_seeder
from infrastructure.database.seeders.organization_members_seeder import organization_members_seeder
from infrastructure.database.seeders.event_speaker_seeder import event_speaker_seeder
from infrastructure.database.seeders.transactions_seeder import transactions_seeder
from infrastructure.database.seeders.tickets_seeder import tickets_seeder
from infrastructure.config.database import get_db

async def run_seeders():
    try:
        async for db in get_db():
            async with db:
                await seed_user(db)
                await participant_seeder(db)
                await organization_members_seeder(db)
                await event_seeder(db)
                await event_speaker_seeder(db)
                await transactions_seeder(db)
                await tickets_seeder(db)
                await db.commit()
                print("Seeding completed successfully!")
    except Exception as e:
        print(e)
        if isinstance(db, AsyncSession):
            await db.rollback()
            print(f"Error running seeders: {e}")
    finally:
        await db.aclose()
        print("Seeding process completed!")


if __name__ == "__main__":
    try:
        asyncio.run(run_seeders())
    except RuntimeError as e:
        print(f"RuntimeError: {e}")

