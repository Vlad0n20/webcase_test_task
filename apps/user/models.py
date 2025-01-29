from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager


class User(AbstractUser):
    username = None
    email = models.EmailField('Email', unique=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('-id',)
