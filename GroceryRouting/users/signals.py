from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from routing.models import *
from datetime import date
from random import randrange,random

@receiver(post_save, sender = User)
def create_session(sender, instance, created, **kwargs):
	if created:
		sess = Session()
		sess.user = instance 
		sess.session = 0 
		sess.delivery_date = date.today()
		sess.homes = 25
		sess.agents = 10
		sess.warehouse_latitude = 28.5531
		sess.warehouse_longitude = 77.2046
		sess.save()
		Home.objects.create(latitude= 28.5359, longitude = 77.2209, demand=15,number=1, session = sess, user=instance)
		Home.objects.create(latitude= 28.522, longitude = 77.2193, demand=12,number=2, session = sess, user=instance)
		Home.objects.create(latitude= 28.5396, longitude = 77.2329, demand=13,number=3, session = sess, user=instance)
		Home.objects.create(latitude= 28.5695, longitude = 77.2186, demand=17,number=4, session = sess, user=instance)
		Home.objects.create(latitude= 28.5229, longitude = 77.1907, demand=2,number=5, session = sess, user=instance)
		Home.objects.create(latitude= 28.5372, longitude = 77.1775, demand=9,number=6, session = sess, user=instance)
		Home.objects.create(latitude= 28.5541, longitude = 77.2181, demand=13,number=7, session = sess, user=instance)
		Home.objects.create(latitude= 28.5661, longitude = 77.1985, demand=3,number=8, session = sess, user=instance)
		Home.objects.create(latitude= 28.5325, longitude = 77.2497, demand=8,number=9, session = sess, user=instance)
		Home.objects.create(latitude= 28.5385, longitude = 77.234, demand=1,number=10, session = sess, user=instance)
		Home.objects.create(latitude= 28.5242, longitude = 77.1915, demand=0,number=11, session = sess, user=instance)
		Home.objects.create(latitude= 28.5548, longitude = 77.2418, demand=17,number=12, session = sess, user=instance)
		Home.objects.create(latitude= 28.5472, longitude = 77.204, demand=5,number=13, session = sess, user=instance)
		Home.objects.create(latitude= 28.5465, longitude = 77.1955, demand=9,number=14, session = sess, user=instance)
		Home.objects.create(latitude= 28.5462, longitude = 77.1986, demand=18,number=15, session = sess, user=instance)
		Home.objects.create(latitude= 28.5363, longitude = 77.228, demand=5,number=16, session = sess, user=instance)
		Home.objects.create(latitude= 28.5208, longitude = 77.2324, demand=14,number=17, session = sess, user=instance)
		Home.objects.create(latitude= 28.5407, longitude = 77.2537, demand=2,number=18, session = sess, user=instance)
		Home.objects.create(latitude= 28.5551, longitude = 77.2479, demand=16,number=19, session = sess, user=instance)
		Home.objects.create(latitude= 28.5365, longitude = 77.2177, demand=0,number=20, session = sess, user=instance)
		Home.objects.create(latitude= 28.5236, longitude = 77.2319, demand=13,number=21, session = sess, user=instance)
		Home.objects.create(latitude= 28.5458, longitude = 77.1761, demand=15,number=22, session = sess, user=instance)
		Home.objects.create(latitude= 28.5258, longitude = 77.2553, demand=16,number=23, session = sess, user=instance)
		Home.objects.create(latitude= 28.558, longitude = 77.2228, demand=14,number=24, session = sess, user=instance)
		Home.objects.create(latitude= 28.5657, longitude = 77.2379, demand=3,number=25, session = sess, user=instance)
		DeliveryAgent.objects.create(capacity=16, number=1, session = sess, user=instance)
		DeliveryAgent.objects.create(capacity=31, number=2, session = sess, user=instance)
		DeliveryAgent.objects.create(capacity=9, number=3, session = sess, user=instance)
		DeliveryAgent.objects.create(capacity=7, number=4, session = sess, user=instance)
		DeliveryAgent.objects.create(capacity=39, number=5, session = sess, user=instance)
		DeliveryAgent.objects.create(capacity=31, number=6, session = sess, user=instance)
		DeliveryAgent.objects.create(capacity=37, number=7, session = sess, user=instance)
		DeliveryAgent.objects.create(capacity=50, number=8, session = sess, user=instance)
		DeliveryAgent.objects.create(capacity=18, number=9, session = sess, user=instance)
		DeliveryAgent.objects.create(capacity=36, number=10, session = sess, user=instance)
		
@receiver(post_save, sender = Session)
def edit_profile(sender, instance, created, **kwargs):
	if created:
		try:
			prof = instance.user.profile
			prof.last_session = instance
			prof.save()
		except Profile.DoesNotExist:
			Profile.objects.create(user = instance.user, last_session = instance)

#@receiver(post_save, sender = User)
#ef save_profile(sender, instance, created, **kwargs):
#	instance.profile.save()
