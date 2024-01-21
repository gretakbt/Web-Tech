
from django.contrib import admin
from django.urls import path, include

from poll import views as poll_views
from  todolist import views as todolist_views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views




urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', poll_views.polls, name='polls'),
    path('group/<int:group_id>/create/', poll_views.create, name='create'),
    path('results/<poll_id>/', poll_views.results, name='results'),
    path('vote/<poll_id>/', poll_views.vote, name='vote'),
    path('polls/<int:poll_id>/delete/', poll_views.delete_poll, name='delete_poll'),
    path('accounts/login/', todolist_views.CustomLoginView.as_view(), name='login'),
    path('password_reset/', todolist_views.reset_password, name='reset password'),##
    path('password_reset/done/', todolist_views.password_reset_done, name='password_reset_done'),
    path('reset/password/complete/', todolist_views.CustomPasswordResetDoneView.as_view(), name='password_reset_complete'), 
    path('reset/password/confirm/<str:uidb64>/<str:token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),##
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('registration', todolist_views.register, name='register'), ##
    path('', todolist_views.CombinedView.as_view(), name='calendar'),
    path('task/<int:pk>/', todolist_views.TaskDetail.as_view(), name='task'),
    path('task-create/', todolist_views.TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', todolist_views.TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', todolist_views.DeleteView.as_view(), name='task-delete'),
    path('task-reorder/', todolist_views.TaskReorder.as_view(), name='task-reorder'),
    path('group/', todolist_views.GroupListView.as_view(), name='group'),
    path('group/<int:group_id>/', todolist_views.group_detail, name='group_detail'),
    path('create_group/', todolist_views.create_group, name='create_group'),
    path('group/<int:group_id>/leave/', todolist_views.leave_group, name='leave_group'),
    path('group/<int:group_id>/add_member/', todolist_views.add_member, name='add_member'),
    path('event/new/', todolist_views.event_new, name='event_new'),
    path('event/edit/<int:event_id>/', todolist_views.event_edit, name='event_edit'),
    path('event/delete/<int:event_id>/', todolist_views.event_delete, name='event_delete'),
    path('day/(?P<month>\d+)/(?P<year>\d+)/(?P<day>\d+)/', todolist_views.show_day, name='show_day'),
    path('yearly_view/', todolist_views.yearly_view, name='yearly_view'),
    path('change_view/', todolist_views.change_view, name='change_view'),
    path('find_timeslots/<int:group_id>/', todolist_views.display_events, name='find_timeslots'),
    path('group/<int:group_id>/', todolist_views.group_detail, name='group_detail'),

]



