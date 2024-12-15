from domain.repositories.user.user_repository import UserRepository
from domain.repositories.participant.participant_repository import ParticipantRepository
from domain.repositories.event.main import EventRepository
from domain.entities.result.result import Result, Failed, Success
from domain.params.event.main import RegistrationEventParams
from domain.repositories.event_organizer.event_organizer_repository import EventOrganizerRepository
from domain.repositories.ticket.ticket_repository import TicketRepository
from domain.repositories.transaction.transaction_repository import TransactionRepository
from domain.repositories.event_participant.event_participant_repository import EventParticipantRepository

class RegistrationEventUseCase:
    def __init__(self, 
                 user_repository: UserRepository, 
                 event_repository: EventRepository, 
                 event_organizer_repository: EventOrganizerRepository,
                 ticket_repository: TicketRepository,
                 event_participant_repository: EventParticipantRepository,
                 transaction_repository: TransactionRepository,
                 participant_repository: ParticipantRepository):
         self.user_repository = user_repository
         self.event_participant_repository = event_participant_repository
         self.event_organizer_repository = event_organizer_repository
         self.ticket_repository = ticket_repository
         self.transaction_repository = transaction_repository
         self.participant_repository = participant_repository
         self.event_repository = event_repository

    async def call(self, params: RegistrationEventParams) -> Result[dict]:
            try:
                participant = await self.participant_repository.get_participant_by_participant_id(participant_id=params.participant_id)

                if participant is None:
                    return Failed(message="Participant not found")
                
                participant_user = await self.user_repository.get_user_by_user_id(user_id=participant["user_id"])

                if participant_user.is_failed():
                    return Failed(message="Participant user not found")
                
                participant_user = participant_user.result_value()

                event = await self.event_repository.get_event(event_id=params.event_id)

                if event is None:
                    return Failed(message="Event not found")
                
                transaction = await self.transaction_repository.create_transaction(participant_id=participant["participant_id"], amount=event.ticket_price, title="PEMBELIAN TIKET " + event.title)

                if not transaction:
                    return Failed(message="Transaction failed")

                is_success_subtract_participant_balance = await self.participant_repository.subtract_balance(participant_id=participant["participant_id"], amount=event.ticket_price)

                if not is_success_subtract_participant_balance:
                    return Failed(message="Subtract participant balance failed")
                
                ticket = await self.ticket_repository.create_ticket(event_id=params.event_id, transaction_id=transaction["transaction_id"])

                if not ticket:
                    return Failed(message="Ticket failed")
                
                is_success_create_event_participant = await self.event_participant_repository.create_event_participant(participant_id=participant["participant_id"], event_id=params.event_id, ticket_id=ticket["ticket_id"])

                if not is_success_create_event_participant:
                    return Failed(message="Create event participant failed")

                is_success_subtract_ticket = await self.event_repository.substract_ticket(event_id=params.event_id)

                if not is_success_subtract_ticket:
                    return Failed(message="Subtract ticket failed")
                
                is_success_add_balance = await self.event_organizer_repository.add_balance(event_organizer_id=event.event_organizer_id, amount=event.ticket_price)

                if not is_success_add_balance:
                    return Failed(message="Add balance failed")
                
                return Success(value=ticket)

            except ValueError as e:
                return Failed(message=str(e))
            except Exception as e:
                return Failed(message=str(e))