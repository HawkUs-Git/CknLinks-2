from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
class Link(models.Model):
  owner = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
  url = models.CharField(max_length=1000, default="error")
  title = models.CharField(max_length=1000, default="Link title")
  slug = models.CharField(max_length=6, default="ERROR")
  private = models.BooleanField(default=True)
  clicks = models.IntegerField(default=0)

class Click(models.Model):
  link = models.ForeignKey(Link, default=1, on_delete=models.CASCADE)
  clicked = models.DateTimeField(auto_now_add=True)