from sqlalchemy import select
from packages.shared.db import Session
from src.entities.user import User
from src.user.user_interface import IFUserService


class UserService(IFUserService):
    
    async def find_by_id(self, user_id: str) -> User | None:
        async with Session() as session:
            async with session.begin():
                search_user = await session.execute(
                    select(User).where(User.misskey_id == user_id)
                )
        return search_user.scalar_one_or_none()

    async def create(self, misskey_id: str) -> User:
        already_check = await self.find_by_id(misskey_id)
        if already_check:
            return already_check
        async with Session() as session:
            async with session.begin():
                created_user = User(misskey_id=misskey_id)
                session.add(created_user)
        return created_user
