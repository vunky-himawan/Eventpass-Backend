from typing import Type, TypeVar

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.config.database import Base

T = TypeVar('T', bound=Base)

class CountPage:
    def __init__(
            self, 
            modelToCountPage: Type[T],
            db: AsyncSession,
            page_size: int = 10
    ):
        self.modelToCountPage = modelToCountPage
        self.db = db
        self.page_size = page_size

    async def count(self):
        try:
            query = select(func.count()).select_from(self.modelToCountPage)
            statement = await self.db.execute(query)
            count = statement.scalars().first()

            pages = 1
            if count and count > 1:
                pages = (count + self.page_size - 1) // self.page_size if count > 0 else 1
            return pages
        except Exception as e:
            print(f"Error counting: {e}")
            raise e

    async def count_by(self, field: str, value: str):
        try:
            query = select(
                    func.count()
                    ).select_from(
                            self.modelToCountPage
                            ).where(
                                    getattr(
                                        self.modelToCountPage, 
                                        field
                                    ) == value
                            )
            statement = await self.db.execute(query)
            count = statement.scalars().first()

            pages = 1
            if count and count > 1:
                pages = (count + self.page_size - 1) // self.page_size if count > 0 else 1
            return pages
        except Exception as e:
            print(f"Error counting by {field}: {e}")
            raise e
