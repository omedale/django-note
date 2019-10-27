from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from notes import views

urlpatterns = [
    path('users/', views.SignUpAPIView.as_view()),
    path('users/login/', views.LoginAPIView.as_view()),
    path('notes/<int:pk>/', views.NoteDetail.as_view()),
    path('notes/', views.NoteCreateList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)