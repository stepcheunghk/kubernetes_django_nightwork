from django.urls import path
from django.conf.urls import url
from . import views as login_views
from operation import views as op_views
import datetime

urlpatterns = [
    path('', op_views.HomeListView.as_view(), name='home'),
    path('home/', op_views.HomeListView.as_view(), name='home'),
    path('home/test', op_views.HomeTestListView.as_view(), name='homeTest'),
    path('operation/', op_views.operation, name='operation'),
    path('history/', op_views.HistoryListView.as_view(), name='history'),
    path('domain/<str:domain>/', op_views.DomainListView.as_view(), name='domain'),
    path('result/<slug:pk>', op_views.ResultListView.as_view(), name='result'),
    path('application/<slug:id>', op_views.application, name='application'),
    path('plannedmain/<slug:id>', op_views.plannedmain, name='plannedmain'),
    path('edit/<slug:id>', op_views.update, name='edit'),
    path('export/', op_views.export, name='export'),
    path('summary/', op_views.chart, name='summary'),
    path('dateInput/', op_views.dateInput, name='dateInput'),
    path('dateInput/success/', op_views.DateInputSuccessListView.as_view(), name='dateInputSuccess'),
    path('api/operation/', op_views.apiOps, name='apiOps'),
    path('api/dateinput/', op_views.apiDate, name='apiDate'),
]