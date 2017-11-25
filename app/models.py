from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.conf import settings
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class UserRegister(models.Model):
    user = models.OneToOneField(User)
    profile_image = models.FileField(null=False)

    class Meta:
        verbose_name = "Register"
        verbose_name_plural = "Registes"

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
