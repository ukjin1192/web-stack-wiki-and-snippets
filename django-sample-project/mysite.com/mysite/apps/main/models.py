#!usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _


class MyUserManager(BaseUserManager):
    """
    Use email as unique username
    """
    
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password
        """
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            email=self.normalize_email(email),
        )
        
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        
        return user


class Users(AbstractBaseUser):
    """
    User profile which extends AbstracUser
    AbstractBaseUser contains basic fields like password and last_login
    """
    email = models.EmailField(
        verbose_name = _('Email'),
        max_length = 255,
        unique = True
    )
    username = models.CharField(
        verbose_name = _('Username'),
        max_length = 30,
        unique = True,
        null = False
    )
    is_active = models.BooleanField(
        verbose_name = _('Active'),
        default = True
    )
    date_joined = models.DateTimeField(
        verbose_name = _('Joined datetime'),
        auto_now_add = True,
        editable = False
    )

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profile')
        ordering = ['-id']   

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __unicode__(self):
        return unicode(self.email) or u''

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin
