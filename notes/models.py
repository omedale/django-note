from django.db import models
import jwt
from django.contrib.auth.models import UserManager
from datetime import datetime, timedelta
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings

class User(AbstractBaseUser, PermissionsMixin):
  username = models.CharField(db_index=True, max_length=255, unique=True)
  email = models.EmailField(db_index=True, unique=True)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username']

  objects = UserManager()

  def __str__(self):
    return self.email

  @property
  def token(self):
    return self._generate_jwt_token()

  def _generate_jwt_token(self):
    """
    Generates a JSON Web Token that stores this user's ID and has an expiry
    date set to 60 days into the future.
    """
    dt = datetime.now() + timedelta(days=1)

    token = jwt.encode({
        'id': self.pk,
        'exp': int(dt.strftime('%s'))
    }, settings.SECRET_KEY, algorithm='HS256')

    return token.decode('utf-8')


class Note(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  title = models.CharField(max_length=100)
  body = models.TextField()
  owner = models.ForeignKey(User, on_delete=models.CASCADE)

  class Meta:
    ordering = ['created']

  def __str__(self):
    return self.title
  
  def save(self, *args, **kwargs):  
    super(Note, self).save(*args, **kwargs)