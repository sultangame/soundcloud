from .repository import SQLAlchemyRepository
from .dependencies import detail_or_not_found


class Service:
    def __init__(self, repository: SQLAlchemyRepository):
        self.repository: SQLAlchemyRepository = repository()

    async def find_all_joined(self, join):
        answer = await self.repository.find_all_joined(
            join=join
        )
        return answer

    async def find_one_joined(self, pk: int, join):
        answer = await self.repository.find_one_joined(
            join=join, pk=pk
        )
        return await detail_or_not_found(detail=answer)

    async def add_one(self, data):
        answer = await self.repository.add_one(data=data)
        return answer

    async def edit_one(
            self,
            schemas,
            join,
            pk: int,
            partial: bool = False,
    ):
        data = schemas.model_dump(exclude_unset=partial)
        await self.repository.edit_one(pk=pk, data=data)
        answer = await self.repository.find_one_joined(
            join=join, pk=pk
        )
        return await detail_or_not_found(detail=answer)

    async def delete_one(self, pk: int):
        await self.repository.delete_one(pk=pk)
        return {"Message": "Deleted"}
