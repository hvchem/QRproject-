from datetime import timezone
from typing import Any
from django.db import models
from django.contrib.auth.models import   BaseUserManager , AbstractBaseUser , PermissionsMixin
from django.utils import timezone
from hitcount.models import HitCountMixin, HitCount

# Create your models here.




class UserManager(BaseUserManager):
    def create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError("you have not provided a valid email ")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self , email, password, **extra_fields):
        user = self.create_user(email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

class User(AbstractBaseUser,PermissionsMixin):
    
    email = models.EmailField(blank=False , default='',unique=True)
    first_name = models.CharField(max_length=255, blank=False, default='')
    last_name = models.CharField(max_length=255, blank=False, default='')
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    image = models.FileField(upload_to="img", null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    objects = UserManager()
    

class QRstatus(models.Model):
    views = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Views: {self.views}"
    
    
        
    
    
class QRcode(models.Model):
    url = models.URLField(max_length=200)
    title = models.CharField(max_length=50 , default='QRcode name',null=False )
    QRstatus = models.ForeignKey(QRstatus, null = True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    page = models.URLField(max_length=200 , default='')
    def __str__(self):
        return self.url
    