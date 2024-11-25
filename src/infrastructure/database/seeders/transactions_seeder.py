from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from infrastructure.database.models.participant import ParticipantModel
from infrastructure.database.models.transaction import TransactionModel, TransactionCategoryEnum, TransactionStatusEnum

async def transactions_seeder(db: AsyncSession):
    try:
        query = select(ParticipantModel)
        result = await db.execute(query)
        participants = result.scalars().all()

        for participant in participants:
            new_transaction = TransactionModel(
                participant_id=participant.participant_id,
                title="Tiket",
                amount=0,
                category=TransactionCategoryEnum.TIKET.value,
                status=TransactionStatusEnum.BERHASIL.value
            )

            db.add(new_transaction)

        await db.commit()
        await db.refresh(new_transaction)

    except Exception as e:
        await db.rollback()
        print("Error seeding transactions:", e)