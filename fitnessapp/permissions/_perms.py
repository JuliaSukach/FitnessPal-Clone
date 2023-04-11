from ._base import AbstractPermission
from fitnessapp.api.user.models import UserStatus

__all__ = ('Admin', 'Staff', 'Simple')


class Admin(AbstractPermission):
    perms = [UserStatus.ADMIN.name]


class Staff(AbstractPermission):
    perms = [UserStatus.STAFF.name, UserStatus.ADMIN.name]


class Simple(AbstractPermission):
    perms = [st.name for st in UserStatus]
