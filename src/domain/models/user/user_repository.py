from sqlalchemy import select
from src.domain.models.user.user_if import IUserCreateRepository
from src.domain.models.shared.user import User
from src.db import session


class UserRepository(IUserCreateRepository):
    async def find_by_misskey_user_id(self, misskey_id: str) -> User | None:
        async with session() as _session:
            async with _session.begin():
                search_user = await _session.execute(
                    select(User).where(User.misskey_id == misskey_id)
                )
        return search_user.scalar_one_or_none()

    async def create(self, misskey_id: str) -> User:
        already_check = await self.find_by_misskey_user_id(misskey_id)
        if already_check:
            return already_check
        async with session() as _session:
            async with _session.begin():
                created_user = User(misskey_id=misskey_id)
                _session.add(created_user)
        return created_user
