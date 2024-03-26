from src.config.crud import SQLAlchemyRepository
from src.auth import User, Links, Profiles
from sqlalchemy import select
from sqlalchemy.orm import joinedload


class UserRepository(SQLAlchemyRepository):
    model = User

    async def find_all_3_joined(self, join, join2, join3):
        stmt = select(self.model).options(
            joinedload(join)
        ).options(joinedload(join2)).options(
            joinedload(join3)
        )
        result = await self.session.execute(stmt)
        return result.scalars().unique()

    async def find_one_3_joined(self, join, join2, join3, pk: int):
        stmt = select(self.model).options(
            joinedload(join)
        ).options(joinedload(join2)).options(
            joinedload(join3)
        ).where(self.model.id == pk)
        result = await self.session.execute(stmt)
        return result.scalar()


class ProfilesRepository(SQLAlchemyRepository):
    model = Profiles


class LinksRepository(SQLAlchemyRepository):
    model = Links
