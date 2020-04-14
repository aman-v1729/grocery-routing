from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from .forms import *
from django.forms import modelformset_factory
from .helpers import *
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from users.models import *
from .models import *
from django.urls import reverse_lazy
import json
from django.views.decorators.http import require_http_methods
from random import randrange
from datetime import timedelta
from extra_views import ModelFormSetView

sample_coords = [(28.5531,77.2046)]
for i in range(24):
	sample_coords.append((randrange(285200, 285700, 1)/10000, randrange(771720, 772570)/10000))


class AgentResult():
	def __init__(self, disttemp, loadtemp, routetemp, capacitytemp):
		self.distance = disttemp
		self.load = loadtemp
		self.route = routetemp
		self.size = len(routetemp)-1
		self.capacity = capacitytemp

class Node():
	def __init__(self, lattemp, lngtemp, demandtemp, numbertemp):
		self.lat = lattemp
		self.lng = lngtemp
		self.demand = demandtemp
		self.number = numbertemp

def home(request):
	return render(request, 'routing/home.html')

class Solve(LoginRequiredMixin, CreateView):
	model = Session
	form_class = SessionForm
	template_name = 'routing/solve.html'

	def form_valid(self, form):
		form.instance.session = self.request.user.profile.last_session.session + 1
		form.instance.user = self.request.user
		return super().form_valid(form)

	def get_success_url(self):
		return reverse_lazy('routing-solve-homes')

class HomeDataAdd(LoginRequiredMixin, ModelFormSetView):
	model = Home
	template_name = 'routing/home_data.html'
	fields = ['latitude', 'longitude', 'demand']

	def get_factory_kwargs(self):
		kwargs = super(HomeDataAdd, self).get_factory_kwargs()
		kwargs['extra'] = self.request.user.profile.last_session.homes
		return kwargs

	def get_queryset(self):
		return self.model.objects.none()

	def formset_valid(self, formset):
		instances = formset.save(commit = False)
		ct = 0
		for instance in instances:
			ct += 1
			instance.session = self.request.user.profile.last_session
			instance.user = self.request.user
			instance.number = ct
			instance.save()
		return super().formset_valid(formset)
	
	def get_success_url(self):
		return reverse_lazy('routing-solve-agents')

class AgentDataAdd(LoginRequiredMixin, ModelFormSetView):
	model = DeliveryAgent
	template_name = 'routing/agent_data.html'
	fields = ['capacity',]
	def get_factory_kwargs(self):
		kwargs = super(AgentDataAdd, self).get_factory_kwargs()
		kwargs['extra'] = self.request.user.profile.last_session.agents
		return kwargs

	def get_queryset(self):
		return self.model.objects.none()

	def formset_valid(self, formset):
		instances = formset.save(commit = False)
		ct = 0
		for instance in instances:
			ct += 1
			instance.session = self.request.user.profile.last_session
			instance.user = self.request.user
			instance.number = ct
			instance.save()
		return super().formset_valid(formset)

	def get_success_url(self):
		return reverse_lazy('routing-result', kwargs = {'session_num': self.request.user.profile.last_session.session})

def result(request, session_num):
	if request.user.is_authenticated:
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
	try:
		if not request.user.is_authenticated:
			curr_session = Session.objects.get(user = User.objects.get(username = 'b'), session = 0)
		else:
			curr_session = Session.objects.get(user = request.user, session = session_num)
		homes = Home.objects.filter(session = curr_session).order_by('number')
		agents = DeliveryAgent.objects.filter(session = curr_session).order_by('number')
		coords = [(curr_session.warehouse_latitude, curr_session.warehouse_longitude)]
		date = curr_session.delivery_date
		date += timedelta(minutes=330)
		demands = [0]
		capacities = []
		for home in homes:
			coords.append((home.latitude, home.longitude))
			demands.append(home.demand)
		for agent in agents:
			capacities.append(agent.capacity)
		context = {
			'homes' : homes,
			'agents' : agents,
			'coords': coords,
			'demands': demands,
			'capacities': capacities,
			'session': session_num,
			'date': date,
			'homesize': len(homes),
			'warehouselat': curr_session.warehouse_latitude,
			'warehouselng': curr_session.warehouse_longitude,
			'agentsnum': len(capacities)
		}
		context['tempresult'] = god(context)
		context['issolution'] = context['tempresult']['check']
		agentswork = []
		for i in range(0, len(context['tempresult']['result'])):
			agent = context['tempresult']['result'][i]
			agentswork.append(AgentResult(agent['distance'], agent['load'], agent['route'], capacities[i]))
		# for agent in context['tempresult']['result']:
		# 	agentswork.append(AgentResult(agent['distance'], agent['load'], agent['route']))
		context['result'] = agentswork
		return render(request, 'routing/result.html', context)
	except Session.DoesNotExist:
		return redirect('routing-home')

def detail(request, session_num, da):
	if(request.method == 'POST'):
		try:
			if not request.user.is_authenticated:
				curr_session = Session.objects.get(user = User.objects.all().last, session = 0)
			else:
				curr_session = Session.objects.get(user = request.user, session = session_num)
			homes = Home.objects.filter(session = curr_session).order_by('number')
			distance = float(request.POST['distance'])
			load = int(request.POST['load'])
			size = int(request.POST['size'])
			route = []
			print(distance, load, size)
			for i in range (2, size+2):
				route.append(Node(homes[int(request.POST[str(i)])-1].latitude, homes[int(request.POST[str(i)])-1].longitude, homes[int(request.POST[str(i)])-1].demand, int(request.POST[str(i)])))
			context = {
				'session': session_num,
				'distance': distance,
				'size': size,
				'load': load,
				'route': route,
				'warehouselat': curr_session.warehouse_latitude,
				'warehouselng': curr_session.warehouse_longitude,
			}
			if(context['size']==-1):
				context['size'] = 0
			return render(request, 'routing/details.html', context)

		except Session.DoesNotExist:
			return redirect('routing-home')
