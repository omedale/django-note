from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from .models import Note, User
from .serializers import NoteSerializer, LoginSerializer, SignUpSerializer
from .renderers import UserJSONRenderer

class SignUpAPIView(APIView):
  permission_classes = (AllowAny,)
  renderer_classes = (UserJSONRenderer,)

  def post(self, request, *args, **kwargs):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
      user = serializer.save()
      serializer = SignUpSerializer(user)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
  permission_classes = (AllowAny,)
  renderer_classes = (UserJSONRenderer,)

  def post(self, request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NoteList(generics.ListCreateAPIView):
  permission_classes = (IsAuthenticated,)
  queryset = Note.objects.all()
  serializer_class = NoteSerializer

class NoteDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Note.objects.all()
  serializer_class = NoteSerializer
