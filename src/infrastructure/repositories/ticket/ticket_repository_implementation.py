from domain.repositories.ticket.ticket_repository import TicketRepository
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from infrastructure.database.models.ticket import TicketModel
from sqlalchemy import select

class TicketRepositoryImplementation(TicketRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_tickets_by_event_id(self, event_id: str | uuid.UUID) -> list[dict]:
        try:
            query = select(TicketModel).where(TicketModel.event_id == event_id)
            results = await self.db.execute(query)
            tickets = results.scalars().all()

            return tickets

        except Exception as e:
            print(f"Error fetching tickets: {e}")
            raise e
        
    async def get_ticket_by_pin(self, pin: str) -> dict:
        try:
            query = select(TicketModel).where(TicketModel.pin == pin)
            result = await self.db.execute(query)
            ticket = result.scalars().first()

            if ticket is None:
                return None
            
            return ticket.to_dict()

        except ValueError as e:
            print(f"Error fetching tickets: {e}")
            raise e
        except Exception as e:
            print(f"Error fetching tickets: {e}")
            raise e