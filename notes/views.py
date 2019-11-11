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

class NoteCreateList(generics.ListCreateAPIView):
  permission_classes = (IsAuthenticated,)
  def get(self, request):
    notes = Note.objects.filter(owner= request.user.id)
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)

  def post(self, request, *args, **kwargs):
    serializer = NoteSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save(owner=self.request.user)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NoteDetail(generics.RetrieveUpdateDestroyAPIView):
  permission_classes = (IsAuthenticated,)
  queryset = Note.objects.all()
  serializer_class = NoteSerializer

  def get(self, request, pk):
    note = self.get_note(pk)

    serializer = NoteSerializer(note)
    return Response(serializer.data)

  def update(self, request, pk):
    note = self.get_note(pk)

    serializer = NoteSerializer(note, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def destroy(self, request, pk):
      note = self.get_note(pk)

      note.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)

  def get_note(self, pk):
    try:
      return self.get_object()
    except Note.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)
