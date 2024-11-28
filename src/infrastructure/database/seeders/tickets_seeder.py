import secrets
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from infrastructure.database.models.transaction import TransactionModel
from infrastructure.database.models.event import EventModel
from infrastructure.database.models.ticket import TicketModel

async def generate_unique_pin(event_id: int, used_pins: set, length: int = 6) -> str:
    while True:
        pin = ''.join(secrets.choice("0123456789") for _ in range(length))
        if pin not in used_pins:
            used_pins.add(pin)
            return pin

async def tickets_seeder(db: AsyncSession):
    try:
        query = select(EventModel).where(EventModel.title == "EcoWorld: Sustainability and Innovation Expo")
        result = await db.execute(query)
        event = result.scalars().first()

        query = select(TransactionModel)
        result = await db.execute(query)
        transactions = result.scalars().all()

        used_pins = set()

        for transaction in transactions:
            pin = await generate_unique_pin(event.event_id, used_pins)

            new_ticket = TicketModel(
                event_id=event.event_id,
                transaction_id=transaction.transaction_id,
                pin=pin,
            )

            db.add(new_ticket)

        await db.commit()
        await db.refresh(new_ticket)

    except Exception as e:
        await db.rollback()
        print("Error seeding tickets:", e)