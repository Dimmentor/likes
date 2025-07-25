from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_content_admin = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
