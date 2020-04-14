from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name = 'routing-home'),
	path('solve/', views.Solve.as_view(), name = 'routing-solve'),
	path('solve/session/new/home/', views.HomeDataAdd.as_view(), name = 'routing-solve-homes'),
	path('solve/session/new/agent/', views.AgentDataAdd.as_view(), name = 'routing-solve-agents'),
	path('result/session/<int:session_num>/', views.result, name = 'routing-result'),
	path('result/session/<int:session_num>/<int:da>/', views.detail, name = 'routing-detail'),
]
