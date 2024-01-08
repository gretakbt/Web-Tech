from datetime import datetime
from datetime import date
from datetime import timedelta, date, datetime as dt
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar

from .models import *
from .utils import Calendar
from .forms import EventForm
import calendar
# Create your views here.

def index(request):
    return redirect('/calendar')

class CalendarView(generic.ListView):
    model = Event
    template_name = 'cal/calendar.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        # Instantiate our calendar class with today's year and date
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def show_day(request, month, year, day):
    month_int = list(calendar.month_name).index(month)
    context = {
        'day': day,
        'events_for_day': Event.objects.filter(start_time__day=day, start_time__year=year, start_time__month=month_int)
    }
    print(context['events_for_day'])
    return render(request, 'cal/show_day.html', context)


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()
        form = EventForm(request.POST or None, instance=instance)
        return render(request, 'cal/edit_event.html', {'form': form})
    
    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('cal:calendar'))
    return render(request, 'cal/edit_event.html', {'form': form})

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def event_new(request):
    start_time = dt.strptime(request.POST['start_time'],"%Y-%m-%dT%H:%M")
    end_time = dt.strptime(request.POST['end_time'],"%Y-%m-%dT%H:%M")
    Event.objects.create(title=request.POST['title'], description=request.POST['description'], start_time=start_time, end_time=end_time, bg_color=request.POST['bg_color'])
    return redirect('/calendar')

def event_delete(request, event_id):
    event = Event.objects.get(id=event_id)
    event.delete()
    return redirect('/calendar')

def yearly_view(request):
    context={
        'today': date.today()
    }
    return render (request, 'cal/yearly_view.html', context)

def change_view(request):
    month = request.POST['month']
    year = request.POST['year']
    return redirect(f"/calendar/?month={year}-{month}")