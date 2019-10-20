from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):

  def create_user(self, username, email, password=None):
    """Create and return a `User` with an email, username and password."""
    if username is None:
        raise TypeError('Users must have a username.')

    if email is None:
        raise TypeError('Users must have an email address.')

    user = self.model(username=username, email=self.normalize_email(email))
    user.set_password(password)
    user.save()

    return user

  def create_superuser(self, username, email, password):
    """
    Create and return a `User` with superuser (admin) permissions.
    """
    if password is None:
        raise TypeError('Superusers must have a password.')

    user = self.create_user(username, email, password)
    user.is_superuser = True
    user.is_staff = True
    user.save()

    return user
    # """
    # Custom user model manager
    # """
    # def create_user(self, email, password, **extra_fields):
    #   """
    #   Create and save a User with the given email and password.
    #   """
    #   if not email:
    #       raise ValueError(_('The Email must be set'))
    #   email = self.normalize_email(email)
    #   user = self.model(email=email, **extra_fields)
    #   user.set_password(password)
    #   user.save()
    #   return user

    # def create_superuser(self, email, password, **extra_fields):
    #   """
    #   Create and save a SuperUser with the given email and password.
    #   """
    #   extra_fields.setdefault('is_staff', True)
    #   extra_fields.setdefault('is_superuser', True)
    #   extra_fields.setdefault('is_active', True)

    #   if extra_fields.get('is_staff') is not True:
    #       raise ValueError(_('Superuser must have is_staff=True.'))
    #   if extra_fields.get('is_superuser') is not True:
    #       raise ValueError(_('Superuser must have is_superuser=True.'))
    #   return self.create_user(email, password, **extra_fields)
