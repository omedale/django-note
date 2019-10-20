from django.db import models

class Note(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  title = models.CharField(max_length=100)
  body = models.TextField()

  class Meta:
    ordering = ['created']

  def __str__(self):
    return self.title