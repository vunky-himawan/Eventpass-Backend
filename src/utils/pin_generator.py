import random
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.models.ticket import TicketModel

async def generate_unique_pin(session: AsyncSession, event_id: str, length: int = 6) -> str:
    while True:
        pin = ''.join([str(random.randint(0, 9)) for _ in range(length)])

        stmt = select(TicketModel).where(TicketModel.event_id == event_id, TicketModel.pin == pin)
        result = await session.execute(stmt)
        existing_pin = result.scalar_one_or_none()

        if not existing_pin:
            return pin
