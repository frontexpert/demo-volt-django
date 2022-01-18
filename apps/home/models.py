# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User, AbstractUser, BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):

    def create_user(self, correo_personal, password=None, is_superuser=False, is_staff=False, is_active=True):
        user = User(correo_personal=correo_personal, is_superuser=is_superuser, is_staff=is_staff, is_active=is_active)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, correo_personal, password=None):
        return self.create_user(correo_personal, password=password, is_superuser=True, is_staff=True, is_active=True)

class Role(models.Model):
    nombre_rol = models.CharField(max_length=30)            # name of role
    description_rol = models.CharField(max_length=100)      # description of role
    estado_rol = models.IntegerField()                      # current status of role
    usuario_creacion = models.IntegerField()                # id of user who create this record
    fecha_creacion = models.DateTimeField()                 # timestamp of record creation
    usuario_actualizacion = models.IntegerField()           # id of user who update this record
    fecha_actualizacion = models.DateTimeField()            # timestamp of record modification
    ip_creacion = models.CharField(max_length=40)           # ip address of computer that send the request to create the record
    ip_actualizacion = models.CharField(max_length=40)      # ip address of computer that send the request to update the record

class User(AbstractBaseUser, PermissionsMixin):
    hash = models.CharField(max_length=200, null=True, blank=True)
    codigo_usuario = models.CharField(max_length=20)        # code of user inside system
    clave_usuario = models.CharField(max_length=20)         # password of user
    dni_usuario = models.CharField(max_length=8)            # national document of user
    nombres_usuario = models.CharField(max_length=100)      # first name of user
    apellido_paterno = models.CharField(max_length=100)     # last name of user. father's lastname
    apellido_materno = models.CharField(max_length=100)     # last name of user. mother's lastname
    tipo_usuario = models.IntegerField(default=1)                    # user is 'Proveedor' or 'Dependencia'.
    correo_empresa = models.EmailField(max_length=255)       # corproate email of user 
    correo_personal = models.EmailField(_('email address'), unique=True, max_length=255)      # personale email of user
    estado_usuario = models.IntegerField(default=1)                  # current status of user. inactive=0. active=1
    usuario_creacion = models.IntegerField(default=0)                # id of user who create this record
    fecha_creacion = models.DateTimeField(null=True)                 # timestamp of record creation 
    usuario_actualizacion = models.IntegerField(default=0)           # id of user who update this record
    fecha_actualizacion = models.DateTimeField(null=True)            # timestamp of record modification
    ip_creacion = models.CharField(max_length=40)           # ip address of computer that send the request to create the record
    ip_actualizacion = models.CharField(max_length=40)      # ip address of computer that send the request to update the record
    role = models.ForeignKey(Role, on_delete=models.DO_NOTHING, default=3) # id of role table
    is_staff = models.BooleanField(_("staf status"), default=False)
    is_active = models.BooleanField(_("active"), default=True)
    is_superuser = models.BooleanField(_("superuser status"), default=False)
    USERNAME_FIELD ="correo_personal"
    objects = UserManager()

