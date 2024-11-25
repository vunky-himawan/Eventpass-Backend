from domain.entities.result.result import Result, Failed, Success
from domain.repositories.ticket.ticket_repository import TicketRepository
from domain.params.attendance.main import PinAttendanceConfirmationParams
from domain.repositories.event.main import EventRepository
from domain.repositories.transaction.transaction_repository import TransactionRepository
from domain.repositories.attendance.attendance_repository import AttendanceRepository
from infrastructure.database.models.attendance import AttendaceMethodEnum, AttendanceStatusEnum

class PinAttendanceConfirmationUseCase:
    def __init__(self,
                 ticket_repository: TicketRepository,
                 event_repository: EventRepository,
                 transaction_repository: TransactionRepository,
                 attendance_repository: AttendanceRepository
                 ):
        self.ticket_repository = ticket_repository
        self.event_repository = event_repository
        self.transaction_repository = transaction_repository
        self.attendance_repository = attendance_repository

    async def call(self, params: PinAttendanceConfirmationParams) -> Result[dict]:
        try:
            ticket = await self.ticket_repository.get_ticket_by_pin(pin=params.pin)

            if ticket is None:
                return Failed(message="Ticket not found")
            
            transaction = await self.transaction_repository.get_transaction_by_transaction_id(transaction_id=ticket["transaction_id"])

            if transaction is None:
                return Failed(message="Transaction not found")
            
            participantId = transaction["participant_id"]

            attendance = await self.attendance_repository.create_attendance(event_id=ticket["event_id"], 
                                                                            receptionist_id=params.receptionist_id, 
                                                                            participant_id=participantId, 
                                                                            attended_method=AttendaceMethodEnum.PIN.value,
                                                                            status=AttendanceStatusEnum.BERHASIL.value)
            
            
            if attendance is None:
                return Failed(message="Attendance not found")
            
            return Success(value=attendance.to_dict())

        except ValueError as e:
            return Failed(message=str(e))
        except Exception as e:
            return Failed(message=str(e))