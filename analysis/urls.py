from django.urls import path

from analysis import views

urlpatterns = [
    path('datasetProblem', views.problem, name='problem'),
    path('datasetGood', views.good, name='good'),
    path('datasetAlert', views.alert, name='alert')
]
