from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth import login

# Imports for Reordering Feature
from django.views import View
from django.shortcuts import redirect
from django.db import transaction

from .models import Task, Group
from .forms import PositionForm, CreateGroupForm

from poll.models import Poll

#von Greta
from .forms import ResetPasswordForm
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode
from django.contrib import messages  # Hinzugefügter Import für Nachrichten
from django.contrib.auth.models import User
from django.utils.html import strip_tags
from django.views.generic import TemplateView

#Calendar

from datetime import timedelta, date, datetime 
from datetime import timedelta, date, datetime as dt
from django.utils.safestring import mark_safe
import calendar

from .models import *
from .utils import Calendar
from .forms import EventForm


class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('calendar')



##von Greta
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            ##email = form.cleaned_data['email']
              
            html_content = render_to_string('registration/emails/registration_email.html', {'user': user})
            text_content = strip_tags(html_content)
            subject = 'Willkommen neuer User'
            recipient_list = [user.email]
            from_email = 'your-email@example.com'
            send_mail(subject, text_content, from_email, recipient_list, html_message=html_content)   
            # Logge den Benutzer nach der Registrierung ein
            login(request, user)
            return redirect('login') 
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form}) 

def password_reset_done(request):
    return render(request, 'registration/password_reset_done.html') 
def password_reset_confirm(request):
    return render(request, 'registration/password_reset_confirm.html') 
class CustomPasswordResetDoneView(TemplateView):
    template_name = 'registration/reset_complete_template.html'

def reset_password(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = get_user_model().objects.get(email=email)

            # Erzeuge einen Token für den Benutzer
            token = default_token_generator.make_token(user)

            # Erzeuge den Zurücksetzungslink
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(f'/reset/password/confirm/{uidb64}/{token}/')

            email_context = {'user': user, 'reset_url': reset_url}
            html_content = render_to_string('registration/emails/password_reset_email.html', email_context)    
            text_content = strip_tags(html_content)
            subject = 'Angeforderter Passwort-Reset'
            from_email = 'your-email@example.com'
            recipient_list = [email]
            send_mail(subject, text_content, from_email, recipient_list, html_message=html_content)

            return HttpResponseRedirect('/password_reset/done/')  # Beispielhafte Weiterleitung nach dem Versenden der E-Mail
    else:
        form = ResetPasswordForm()

    return render(request, 'registration/password_reset_form.html', {'form': form})



#GPT zusammenführen der beiden Funktionen zur Verwendung auf einer Website 
class CombinedView(LoginRequiredMixin, ListView, View):
    model_task = Task
    model_event = Event
    context_object_name_task = 'tasks'
    context_object_name_event = 'events'
    template_name = 'cal/calendar.html'


    def get_date(self, month):
        today = datetime.today()
        if month:
            year, month = map(int, month.split('-'))
            if 1 <= month <= 12:
                return datetime(year, month, 1)
        
        #Wenn der Monat ungültig ist, verwende den aktuellen Monat
        return datetime(today.year, today.month, 1)

    def prev_month(self, d):
        first = d.replace(day=1)
        prev_month = first - timedelta(days=1)
        month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
        return month

    def next_month(self, d):
        days_in_month = calendar.monthrange(d.year, d.month)[1]
        last = d.replace(day=days_in_month)
        next_month = last + timedelta(days=1)
        month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
        return month


    def get(self, request, *args, **kwargs):
        # TaskList logic
        tasks = self.model_task.objects.filter(user=request.user)
        count = tasks.filter(complete=False).count()
        search_input = request.GET.get('search-area') or ''
        if search_input:
            tasks = tasks.filter(title__contains=search_input)

        # CalendarView logic
        d = self.get_date(request.GET.get('month', None))
        cal = Calendar(d.year, d.month, user=request.user)
        events = Event.objects.filter(users=request.user)
        html_cal = cal.formatmonth(withyear=True)

        context = {
            'tasks': tasks,
            'count': count,
            'search_input': search_input,
            'calendar': mark_safe(html_cal),
            'prev_month': self.prev_month(d),
            'next_month': self.next_month(d),
            'events': events,
        }

        return render(request, self.template_name, context)
    

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('calendar')
    template_name = 'task_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('calendar')
    template_name = 'task_form.html'

class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('calendar')
    template_name = 'task_confirm_delete.html'
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)

class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('calendar'))


##ab hier gruppenkonzept
    
class GroupListView(LoginRequiredMixin, ListView):
    model = Group
    template_name = 'group_list.html'
    context_object_name = 'groups'

    def get_queryset(self):
        
        return self.request.user.group_memberships.all()
    

def group_detail(request, group_id):
    group = Group.objects.get(pk=group_id)

    
    if request.user in group.members.all():
        polls = Poll.objects.filter(group=group)
        return render(request, 'group_detail.html', {'group': group, 'polls': polls})
    else:
        
        return redirect('group')  # Hier kannst du den Pfad anpassen
    
def create_group(request):
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)

        if form.is_valid():
            new_group = form.save(commit=False)
            new_group.save()
            new_group.members.add(request.user)
            messages.success(request, 'Die Gruppe wurde erfolgreich erstellt!')
            return redirect('group')
    else:
        form = CreateGroupForm()

    context = {'form': form}
    return render(request, 'create_group.html', context)




def leave_group(request, group_id):
    group = Group.objects.get(pk=group_id)
    user = request.user
    
    # Überprüfen, ob der Benutzer in der Gruppe ist, bevor er sie verlässt
    if user in group.members.all():
        group.members.remove(user)
        if group.members.count() == 0:
             with transaction.atomic():
                # Lösche alle zugehörigen Umfragen (Polls)
                group_polls = group.group_polls.all()
                group_polls.delete()
                group.delete()
        return redirect('calendar')  # Weiterleitung zur Startseite
    else:
        # Benutzer ist nicht in der Gruppe, vielleicht eine Meldung anzeigen
        return redirect('group_detail', group_id=group_id)


def add_member(request, group_id):
    if request.method == 'POST':
        # Benutzername aus dem Formular abrufen
        username = request.POST.get('username', '')

        try:
            user_to_add = User.objects.get(username=username)
            group = Group.objects.get(pk=group_id)

            if user_to_add not in group.members.all():
                group.members.add(user_to_add)
                messages.success(request, f'User "{username}" was successfully added to the group.')
            else:
                messages.warning(request, f'User "{username}" is already in the group.')
        except User.DoesNotExist:
            messages.error(request, f'User "{username}" not found.')

    # Hier kannst du weitere Logik hinzufügen, wenn die Aktion nicht erfolgreich war
    return redirect('group_detail', group_id=group_id)



# Create your views here.




def show_day(request, month, year, day):
    month_int = list(calendar.month_name).index(month)
    events_for_day = Event.objects.filter(users=request.user, start_time__day=day, start_time__year=year, start_time__month=month_int)

    context = {
        'day': day,
        'events_for_day': events_for_day
    }
    print(context['events_for_day'])
    return render(request, 'cal/show_day.html', context)



def event(request, event_id=None):
    instance = Event()

    if event_id:
        instance = get_object_or_404(Event, pk=event_id)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('calendar'))
    else:
        form = EventForm(instance=instance)

    context = {
        'form': form,
        'event': instance,
    }

    return render(request, 'cal/edit_event.html', context)
from django.http import JsonResponse
import json
def event_new(request):
    if request.method == 'POST':
        # Verarbeiten Sie das Formular für ein neues Event
        
        participant_ids = request.POST.getlist('users')  # Wenn es mehrere ausgewählte Teilnehmer gibt

        users = User.objects.filter(id__in=participant_ids)
        start_time = dt.strptime(request.POST['start_time'], "%Y-%m-%dT%H:%M")
        end_time = dt.strptime(request.POST['end_time'], "%Y-%m-%dT%H:%M")
        Event.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            start_time=start_time,
            end_time=end_time,
            bg_color=request.POST['bg_color']
            
        ).users.set(users)
        return redirect(reverse('calendar'))
    else:
        # Anzeigen des Formulars für ein neues Event
        form = EventForm()
    
    
    context = {
        'form': form,
       
    }

    return render(request, 'cal/new_event.html', context)

def event_edit(request, event_id):
    instance = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('calendar'))
    else:
        users = instance.users.values_list('id', flat=True)
        form = EventForm(instance=instance, initial={'participants': users})

    context = {
        'form': form,
        'event': instance,
    }

    return render(request, 'cal/edit_event.html', context)

def event_delete(request, event_id):
    event = Event.objects.get(id=event_id)
    event.delete()
    return redirect('calendar')

def yearly_view(request):
    context={
        'today': date.today()
    }
    return render (request, 'cal/yearly_view.html', context)

def change_view(request):
    month = request.POST['month']
    year = request.POST['year']
    return redirect(f"/calendar/?month={year}-{month}")