from sqlalchemy import select
from packages.shared.domain.models.user.user_if import IFUserRepository
from packages.shared.domain.models.shared.user import User
from packages.shared.db import Session


class UserRepository(IFUserRepository):
    async def find_by_user_id(self, user_id: str) -> User | None:
        async with Session() as session:
            async with session.begin():
                search_user = await session.execute(
                    select(User).where(User.misskey_id == user_id)
                )
        return search_user.scalar_one_or_none()

    async def create(self, misskey_id: str) -> User:
        already_check = await self.find_by_user_id(misskey_id)
        if already_check:
            return already_check
        async with Session() as session:
            async with session.begin():
                created_user = User(misskey_id=misskey_id)
                session.add(created_user)
        return created_user
