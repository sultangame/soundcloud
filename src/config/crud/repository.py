from src.config.database import async_session_factory
from sqlalchemy.orm import joinedload
from sqlalchemy import select, update, delete


class SQLAlchemyRepository:
    model = None
    session = async_session_factory()

    async def find_all_joined(self, join):
        stmt = select(self.model).options(
            joinedload(join)
        )
        result = await self.session.execute(stmt)
        return result.scalars().unique()

    async def find_one_joined(self, join, pk: int):
        stmt = select(self.model).options(
            joinedload(join)
        ).where(self.model.id == pk)
        result = await self.session.execute(stmt)
        return result.scalar()

    async def add_one(self, data):
        self.session.add(data)
        await self.session.commit()
        await self.session.refresh(data)
        return data

    async def edit_one(self, pk: int, data: dict) -> None:
        stmt = update(self.model).where(self.model.id == pk).values(**data)
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete_one(self, pk: int) -> None:
        stmt = delete(self.model).where(
            self.model.id == pk
        )
        await self.session.execute(stmt)
        await self.session.commit()
