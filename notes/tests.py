
from rest_framework import status
from django.urls import reverse
from .models import User, Note
from .serializers import NoteSerializer, LoginSerializer, SignUpSerializer
from rest_framework.test import APITestCase, APIClient

class UserTest(APITestCase):
  def setUp(self):
    self.valid_payload = {
        'email': 'admin@gmail.com',
        'username': 'test',
        'password': 'test3iu3oi'
    }

    self.invalid_payload = {
        'email': 'femi@gmail.com',
        'username': '',
        'password': ''
    }

    self.sign_up_url = reverse('auth-register')
    self.login_url = reverse('auth-login')
    self.client = APIClient()
    self.user = User.objects.create_user(
      email='testuser@test.com',
      username='femi',
      password='test123454',
    )

  def test_sign_up_with_valid_user(self):
    response = self.client.post(
      self.sign_up_url,
      self.valid_payload,
      format='json'
    )
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(response.data['email'], self.valid_payload['email'])

  def test_sign_up_with_invalid_user(self):
    response = self.client.post(
        self.sign_up_url,
        self.invalid_payload,
        format='json'
    )
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  def test_login_with_valid_detail(self):
    response = self.client.post(
      self.login_url,
      {'email': self.user.email, 'password': 'test123454'},
      format='json'
    )
    self.assertEqual(response.status_code, status.HTTP_200_OK)
  
  def test_login_with_invalid_detail(self):
    response = self.client.post(
      self.login_url,
      {'email': 'omeda@yaoo.com', 'password': 'test123454'},
      format='json'
    )
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class NotesTest(APITestCase):
  def setUp(self):
    self.client = APIClient()
    self.create_list_note_url = reverse('note-list')
    self.user = self.setup_user()
    self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user.token)
    self.note = Note.objects.create(title='Title 1', body='Content body', owner=self.user)
    self.valid_note_detail_url = reverse('note-detail', args=[self.note.pk])
    self.invalid_note_detail_url = reverse('note-detail', args=[000])

  @staticmethod
  def setup_user():
    return User.objects.create(
        email='testuser@test.com',
        password='test123454',
        username='femi'
    )
  
  def test_create_note_with_valid_input(self):
    response = self.client.post(self.create_list_note_url, {'title':'Title 2', 'body': 'Content body 3', 'owner': self.user})
    note = Note.objects.get(title='Title 2')
    serializer = NoteSerializer(note)
    self.assertEqual(response.data, serializer.data)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
  
  def test_update_note_with_valid_input(self):
    response = self.client.put(self.valid_note_detail_url, {'title':'Title updated', 'body': 'Updated body',})
    note = Note.objects.get(title='Title updated')
    serializer = NoteSerializer(note)
    self.assertEqual(response.data, serializer.data)
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

  def test_create_note_with_invalid_input(self):
    response = self.client.post(self.create_list_note_url, {})
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  def test_note_list(self):
    response = self.client.get(self.create_list_note_url)
    notes = Note.objects.all()
    serializer = NoteSerializer(notes, many=True)
    self.assertEqual(response.data, serializer.data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_valid_note_detail(self):
    response = self.client.get(self.valid_note_detail_url)
    note = Note.objects.get(pk=self.note.pk)
    serializer = NoteSerializer(note)
    self.assertEqual(response.data, serializer.data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_invalid_note_detail(self):
    response = self.client.get(self.invalid_note_detail_url)
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


  def test_valid_delete_puppy(self):
    response = self.client.delete(self.valid_note_detail_url, kwargs={'pk': self.note.pk})
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

  def test_invalid_delete_puppy(self):
    response = self.client.delete(self.invalid_note_detail_url, kwargs={'pk': 000})
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)