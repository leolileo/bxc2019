from django.urls import path

from frontend import views

urlpatterns = [
    path('', views.index, name='status'),
    path('problem', views.problem, name='problem'),
    path('alert', views.alert, name='alert')
]
