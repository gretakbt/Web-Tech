from django.urls import path
from . import views

app_name = 'cal'
urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'calendar/', views.CalendarView.as_view(), name='calendar'),
    path(r'^event/new/', views.event, name='event_new'),
    path(r'^event/edit/(?P<event_id>\d+)/', views.event, name='event_edit'),
    path(r'^event/delete/(?P<event_id>\d+)/', views.event_delete, name='event_delete'),
    path(r'^calendar/day/(?P<month>\w+)/(?P<year>\w+)/(?P<day>\d+)/', views.show_day, name='show_day'),
    path(r'^calendar/yearly_view/', views.yearly_view, name='yearly_view'),
    path(r'^calendar/change_view/', views.change_view, name='change_view'),


]