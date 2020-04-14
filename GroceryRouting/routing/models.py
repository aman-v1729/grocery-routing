from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Session(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	session = models.IntegerField(default = 0)
	delivery_date = models.DateField(help_text = 'Use MM/DD/YY format')
	homes = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(49)])
	agents = models.IntegerField(validators=[MinValueValidator(1)])
	sesstime = models.DateTimeField(auto_now_add = True)
	warehouse_latitude = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])
	warehouse_longitude = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])

	def __str__(self):
		return f'{self.user}, {self.session}'

class Home(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	session = models.ForeignKey(Session, on_delete=models.CASCADE)
	number = models.IntegerField()
	latitude = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])
	longitude = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])
	demand = models.IntegerField(validators=[MinValueValidator(0)])

	def __str__(self):
		return f'{self.user}, {self.session.session}, {self.number}'
	class Meta:
		constraints	= [
			models.UniqueConstraint(fields = ['session', 'number'], name = 'unique_home'),
		]

class DeliveryAgent(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	session = models.ForeignKey(Session, on_delete=models.CASCADE)
	number = models.IntegerField()
	capacity = models.IntegerField(validators=[MinValueValidator(0)])
	
	class Meta:
		constraints	= [
			models.UniqueConstraint(fields = ['session', 'number'], name = 'unique_agent'),
		]
	def __str__(self):
		return f'{self.user}, {self.session.session}, {self.number}'
