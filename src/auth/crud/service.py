from src.config.crud import Service, detail_or_not_found


class UserService(Service):
    async def find_all_3_joined(self, join, join2, join3):
        users = await self.repository.find_all_3_joined(
            join=join, join2=join2, join3=join3
        )
        return users

    async def find_one_3_joined(self, pk: int, join, join2, join3):
        user = await self.repository.find_one_3_joined(
            join=join, join2=join2, join3=join3, pk=pk
        )
        return await detail_or_not_found(user)
