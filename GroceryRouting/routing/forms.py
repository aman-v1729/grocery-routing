from django import forms
from django.forms import ValidationError
from datetime import datetime,timedelta
from .models import *


class SessionForm(forms.ModelForm):
	
	class Meta:
		model = Session
		fields = ('delivery_date', 'homes', 'agents', 'warehouse_latitude', 'warehouse_longitude')

class HomeForm(forms.ModelForm):
	class Meta:
		model = Home
		fields = ('user', 'session', 'number', 'latitude', 'longitude', 'demand')

class DeliveryAgentForm(forms.ModelForm):
	class Meta:
		model = DeliveryAgent
		fields = ('user', 'session', 'number', 'capacity')
