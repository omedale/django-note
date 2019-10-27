from rest_framework import serializers
from django.db import models
from django.contrib.auth import authenticate

from .models import Note, User

class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'token']


class LoginSerializer(serializers.Serializer):
  email = serializers.CharField(max_length=255)
  username = serializers.CharField(max_length=255, read_only=True)
  password = serializers.CharField(max_length=128, write_only=True)
  token = serializers.CharField(max_length=255, read_only=True)

  def validate(self, data):
    email = data.get('email', None)
    password = data.get('password', None)

    if email is None:
      raise serializers.ValidationError(
          'An email address is required to log in.'
      )
    
    if password is None:
      raise serializers.ValidationError(
          'A password is required to log in.'
      )

    user = authenticate(username=email, password=password)

    if user is None:
      raise serializers.ValidationError(
          'A user with this email and password was not found.'
      )
    
    if not user.is_active:
      raise serializers.ValidationError(
          'This user has been deactivated.'
      )

    return {
            'email': user.email,
            'username': user.username,
            'token': user.token
    }



class NoteSerializer(serializers.ModelSerializer):
  title = serializers.CharField(max_length=120)
  body = serializers.CharField()
  
  class Meta:
    model = Note
    fields = ('id', 'title', 'body','owner',)
    extra_kwargs = {
      'owner' : {'read_only' : True}
    }