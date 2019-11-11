from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from notes import views

urlpatterns = [
    path('users/', views.SignUpAPIView.as_view(), name="auth-register"),
    path('users/login/', views.LoginAPIView.as_view(), name="auth-login"),
    path('notes/<int:pk>/', views.NoteDetail.as_view(), name="note-detail"),
    path('notes/', views.NoteCreateList.as_view(), name="note-list"),
]

urlpatterns = format_suffix_patterns(urlpatterns)