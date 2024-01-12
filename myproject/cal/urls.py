from django.urls import path
from . import views

app_name = 'cal'
urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'calendar/', views.CalendarView.as_view(), name='calendar'),
    path(r'event/new/', views.event_new, name='event_new'),
    path(r'event/edit/<int:event_id>/', views.event_edit, name='event_edit'),
    path(r'event/delete/<int:event_id>/', views.event_delete, name='event_delete'),
    path(r'calendar/day/(?P<month>\d+)/(?P<year>\d+)/(?P<day>\d+)/', views.show_day, name='show_day'),
    path(r'calendar/yearly_view/', views.yearly_view, name='yearly_view'),
    path(r'calendar/change_view/', views.change_view, name='change_view'),


]