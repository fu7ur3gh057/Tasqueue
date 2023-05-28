from typing import Any

from django.contrib.auth.base_user import BaseUserManager

# from apps.users.models import User
from other.enums import RoleType


class UserManager(BaseUserManager):

    def _create_user(self, email: str, password=None) -> Any:
        # if username is None:
        #     raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a email')
        if password is None:
            raise TypeError('Users should have a password')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email: str, phone_number: str, type: str, password=None) -> Any:
        if phone_number is None:
            raise TypeError('Users should have a phone_number')
        role_type = RoleType.CUSTOMER if type == 'customer' else RoleType.WORKER
        user = self._create_user(email=email, password=password)
        user.phone_number = phone_number
        user.role = role_type
        user.save()
        return user

    def create_staff(self, email, password) -> Any:
        user = self._create_user(email, password)
        user.role = RoleType.STAFF
        user.save()
        return user

    def create_superuser(self, email, password) -> Any:
        user = self._create_user(email, password)
        user.is_superuser = True
        user.role = RoleType.ADMIN
        user.save()
        return user
