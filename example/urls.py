from django.urls import path

from example import views

urlpatterns = [
    path('', views.index, name='status'),
    path('problem', views.problem, name='problem'),
    path('alert', views.alert, name='alert')
]
