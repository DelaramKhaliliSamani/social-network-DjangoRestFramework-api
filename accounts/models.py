from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail


class User(AbstractBaseUser):
    staff_id = models.CharField(max_length=11, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=11)
    username = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'staff_id'
    REQUIRED_FIELDS = ['phone_number','email', 'username' ]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin



class Relation(models.Model):
	from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
	to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.from_user} following {self.to_user}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='puser')
    bio = models.TextField(null=True, blank=True)
    img = models.ImageField(upload_to='profile_img/%Y/%m/%d')



class DirectMessage(models.Model):

    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    body = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']


    def __str__(self):
        return f'{self.from_user} seding message to {self.to_user}'





@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """""
      send email = password_reset
      confirm and change password = password_reset/confirm
      """""
    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Company X"),
        # message:
        email_plaintext_message,
        # from:
        "deli.khalili73@gmail.com",
        # to:
        [reset_password_token.user.email]
    )