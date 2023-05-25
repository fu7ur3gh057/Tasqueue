from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        # if username is None:
        #     raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a username')
        # user = self.model(username=username, email=self.normalize_email(email))
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        if password is None:
            raise TypeError('Users should have a password')
        # user = self.create_user(username, email, password)
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
