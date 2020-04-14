from random import randrange,random
from routing.models import *
from django.contrib.auth.models import User
'''
for i in range(25):
	latitude = (randrange(285200, 285700, 1)/10000)
	longitude = (randrange(771720, 772570)/10000)
	demand = int(random()*20)
	print(f'Home.objects.create(latitude= {latitude}, longitude = {longitude}, demand={demand},number={i+1}, session = sess, user=instance)')
for i in range(10):
	cap = int(random()*40)
	print(f'DeliveryAgent.objects.create(capacity={cap}, number={i+1}, session = sess, user=instance)')
'''

b = User.objects.get(username = 'b')
session = Session.objects.get(session = 0, user = b)
Homes = Home.objects.filter(session = session).order_by('number')
Agents = DeliveryAgent.objects.filter(session = session).order_by('number')

for agent in Agents:
	print(f'DeliveryAgent.objects.create(capacity={agent.capacity}, number={agent.number}, session = sess, user=instance)')

for home in Homes:
	print(f'Home.objects.create(latitude= {home.latitude}, longitude = {home.longitude}, demand={home.demand},number={home.number}, session = sess, user=instance)')

