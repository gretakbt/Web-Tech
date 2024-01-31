from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse

from .forms import CreatePollForm
from .models import Poll
from todolist.models import Group

#https://prettyprinted.com/tutorials/creating-a-poll-app-in-django + eigene Anpassung an Gruppenkonzept
def polls(request):
    group = request.user.groups.first()
    polls = Poll.objects.filter(group=group)

    context = {
        'polls' : polls
    }
    return render(request, 'polls.html', context)

def create(request,group_id):
    if request.method == 'POST':
        form = CreatePollForm(request.POST, group_id=group_id)

        if form.is_valid():

            form.instance.group = Group.objects.get(id=group_id) #hier Hilfe von Chat-gpt
            form.save()
            return redirect('group_detail', group_id=group_id)
            
            new_poll.save()

    else:
        form = CreatePollForm(group_id=group_id)

    context = {'form' : form}
    return render(request, 'create.html', context)

def results(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)

    context = {
        'poll' : poll
    }
    return render(request, 'results.html', context)

def vote(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    group_id = poll.group.id

    if request.method == 'POST':

        selected_option = request.POST['poll']
        if selected_option == 'option1':
            poll.option_one_count += 1
        elif selected_option == 'option2':
            poll.option_two_count += 1
        elif selected_option == 'option3':
            poll.option_three_count += 1
        else:
            return HttpResponse(400, 'Invalid form option')
    
        poll.save()

        return redirect('group_detail', group_id=group_id)

    context = {
        'poll' : poll
    }
    return render(request, 'vote.html', context)
#https://prettyprinted.com/tutorials/creating-a-poll-app-in-django + eigene Anpassung an Gruppenkonzept

#Chat GPT + https://stackoverflow.com/questions/524992/how-to-implement-a-back-link-on-django-templates
def delete_poll(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    group_id = poll.group.id
    if request.method == 'POST':
        poll.delete()
        return HttpResponseRedirect(reverse('group_detail', kwargs={'group_id': group_id}))  
    return render(request, 'group.html', {'poll': poll})


