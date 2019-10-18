from django.db import models
from pygments.styles import get_all_styles

STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])

class Note(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  title = models.CharField(max_length=100)
  body = models.TextField()
  style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

  class Meta:
    ordering = ['created']

  def __str__(self):
    return self.title