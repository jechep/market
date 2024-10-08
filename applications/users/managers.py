# django
from typing import Any
from django.db import models
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager, models.Manager):
    
    def _create_user(self, username, email, password, is_staff, is_superuser, is_active=True, **extra_fields):
        '''
            Crea y guarda un usuario con los datos dados
        '''

        user = self.model(
            username=username,
            email=email,
            is_active=is_active,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False, True, **extra_fields)
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, True, True, True, **extra_fields)
    
    def users_sistema(self):
        return self.filter(
            is_superuser=False
        ).order_by('-last_login')