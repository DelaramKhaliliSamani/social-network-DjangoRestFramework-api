from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, staff_id, phone_number, email, username, password):
        if not staff_id:
            raise ValueError('Users must have a id')
        if not phone_number:
            raise ValueError('Users must have a phone number')
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a full name')

        user = self.model(staff_id=staff_id, phone_number=phone_number, email=self.normalize_email(email), username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, staff_id, phone_number, email, username, password):
        user = self.create_user(staff_id, phone_number, email, username, password)
        user.is_admin = True
        user.save(using=self._db)
        return user