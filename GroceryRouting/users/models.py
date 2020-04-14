from django.db import models
from django.contrib.auth.models import User
from routing.models import Session
# Create your models here.

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	last_session = models.ForeignKey(Session, on_delete=models.CASCADE)
	
	def __str__(self):
		return f'{self.user}'