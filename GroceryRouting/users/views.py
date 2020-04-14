from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from routing.models import *
from datetime import date
import datetime
from django.utils import timezone
from datetime import timedelta

def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'account created for {username}!')
			return redirect('login')
	else:
		form=UserCreationForm()
	return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
	sessions = Session.objects.filter(user = request.user).order_by('-session')
	ct = 0
	first = second = fl = 0
	for sess in sessions:
		ct += 1
		if ct == 1:
			first = sess
		else:
			agents = len(DeliveryAgent.objects.filter(session = sess))
			homes = len(Home.objects.filter(session = sess))
			if agents < sess.agents or homes < sess.homes:
				sess.delete()
			elif fl == 0:
				second = sess
				fl = 1

	agents = len(DeliveryAgent.objects.filter(session = first))
	homes = len(Home.objects.filter(session = first))
	if agents < first.agents or homes < first.homes:
		prof = request.user.profile
		prof.last_session = second
		prof.save()
		first.delete()

	#MAKE 3 querysets FUTURE TODAY PAST filter using dates(from datetime import date karke and teeno databases bana aur unki lengths le.
	#if 0 then write no deliveries otherwise show the activity for all three.
	#TOP pe TODAY, then Future the Past use session.delivery_date.......
	#for the creation of the object(that is form filling time use session.sessdate))ORDER KARLENA BY session.
	#Don't touch upar wala code only write below this comment
	#don't forget to .exclude(session = 0)
	#admin wale mein im making objects 1 1 ke using various dates. for testing :)
	future = []
	past = []
	today = []
	sessions = Session.objects.filter(user = request.user).exclude(session = 0).order_by('-delivery_date')
	for session in sessions:
		session.sesstime += timedelta(minutes=330)
		session.delivery_date += timedelta(minutes=330)
		if(session.delivery_date>date.today()):
			future.append(session)
		elif(session.delivery_date<date.today()):
			past.append(session)
		else:
			today.append(session)
	today.reverse()
	future.reverse()
	context = {
		'sessions': sessions,
		'future': future,
		'past': past,
		'today': today,
		'todaylen': len(today),
		'futurelen': len(future),
		'pastlen': len(past)
	}
	print(today, past, future)
	print(timezone.now())
	return render(request, 'users/profile.html', context)
