from __future__ import annotations

from enum import Enum
from typing import Union

from discord import Member, User
from discord.ext.commands import check, Context, CheckFailure
from sqlalchemy import Column, String, Integer

from PyDrocsid.database import db, db_thread
from PyDrocsid.translations import translations


class PermissionModel(db.Base):
    __tablename__ = "permissions"

    permission: Union[Column, str] = Column(String(64), primary_key=True, unique=True)
    level: Union[Column, int] = Column(Integer)

    @staticmethod
    def create(permission: str, level: int) -> "PermissionModel":
        row = PermissionModel(permission=permission, level=level)
        db.add(row)
        return row

    @staticmethod
    def get(permission: str, default: int) -> int:
        if (row := db.get(PermissionModel, permission)) is None:
            row = PermissionModel.create(permission, default)

        return row.level

    @staticmethod
    def set(permission: str, level: int) -> PermissionModel:
        if (row := db.get(PermissionModel, permission)) is None:
            return PermissionModel.create(permission, level)

        row.level = level
        return row


class BasePermission(Enum):
    @property
    def description(self) -> str:
        return self.value

    async def resolve(self) -> BasePermissionLevel:
        from PyDrocsid.config import Config

        value: int = await db_thread(PermissionModel.get, self.name, Config.DEFAULT_PERMISSION_LEVEL.level)
        for level in Config.PERMISSION_LEVELS:  # type: BasePermissionLevel
            if level.level == value:
                return level
        raise ValueError(f"permission level not found: {value}")

    async def set(self, level: BasePermissionLevel):
        await db_thread(PermissionModel.set, self.name, level.level)

    async def check_permissions(self, member: Union[Member, User]) -> bool:
        return await (await self.resolve()).check_permissions(member)

    @property
    def check(self):
        return check_permission_level(self)


class BasePermissionLevel(Enum):
    @property
    def level(self) -> int:
        return self.value[0]

    @property
    def aliases(self) -> list[str]:
        return self.value[1]

    @property
    def description(self) -> str:
        return self.value[2]

    @classmethod
    async def get_permission_level(cls, member: Union[Member, User]) -> BasePermissionLevel:
        raise NotImplementedError

    async def check_permissions(self, member: Union[Member, User]) -> bool:
        level: BasePermissionLevel = await self.get_permission_level(member)
        return level.value >= self.value  # skipcq: PYL-W0143

    @property
    def check(self):
        return check_permission_level(self)


def check_permission_level(level: Union[BasePermission, BasePermissionLevel]):
    @check
    async def inner(ctx: Context):
        member: Union[Member, User] = ctx.author
        if not isinstance(member, Member):
            member = ctx.bot.guilds[0].get_member(ctx.author.id) or member
        if not await level.check_permissions(member):
            raise CheckFailure(translations.not_allowed)

        return True

    return inner