"""poll_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from poll import views as poll_views
from  todolist import views as todolist_views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views



from todolist.views import GroupListView


urlpatterns = [
 path('admin/', admin.site.urls),
    path('polls/', poll_views.polls, name='polls'),
    path('group/<int:group_id>/create/', poll_views.create, name='create'),
    path('results/<poll_id>/', poll_views.results, name='results'),
    path('vote/<poll_id>/', poll_views.vote, name='vote'),
    path('polls/<int:poll_id>/delete/', poll_views.delete_poll, name='delete_poll'),
    path('accounts/login/', todolist_views.CustomLoginView.as_view(), name='login'),
    path('password_reset/', todolist_views.reset_password, name='reset password'),##
    path('password_reset/done/', todolist_views.password_reset_done, name='password_reset_done'), ##
    ##path('password_reset/confirm/', password_reset_confirm, name='password_reset_confirm'),##
    path('reset/password/confirm/<str:uidb64>/<str:token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),##
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    ##path('register/', todolist_views.RegisterPage.as_view(), name='register'),
    path('registration', todolist_views.register, name='register'), ##
    path('', todolist_views.TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', todolist_views.TaskDetail.as_view(), name='task'),
    path('task-create/', todolist_views.TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', todolist_views.TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', todolist_views.DeleteView.as_view(), name='task-delete'),
    path('task-reorder/', todolist_views.TaskReorder.as_view(), name='task-reorder'),
    path('group/', todolist_views.GroupListView.as_view(), name='group'),
    path('group/<int:group_id>/', todolist_views.group_detail, name='group_detail'),
    path('create_group/', todolist_views.create_group, name='create_group'),
]



