from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse

from .forms import CreatePollForm
from .models import Poll
from todolist.models import Group

#alle angepasst um Gruppen zu ermöglichen
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
           
        
            # Weise die Gruppe der Umfrage zu und speichere sie
            form.instance.group = Group.objects.get(id=group_id)
            form.save()
            return redirect('group_detail', group_id=group_id)
            ##new_poll = form.save(commit=False)

            # Extrahiere die Gruppe direkt aus dem Formular
            ##group = new_poll.group

            # Speichere das Poll-Objekt
            new_poll.save()

            # Leite zur Gruppendetailansicht weiter
            ##return redirect('group_detail', group_id=group.id)
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

# Chat GPT
def delete_poll(request, poll_id):
    # Umfrageobjekt aus der Datenbank abrufen oder 404-Fehler auslösen
    poll = get_object_or_404(Poll, pk=poll_id)
    group_id = poll.group.id
    if request.method == 'POST':
        # Wenn das Formular gesendet wurde und die Bestätigung erfolgt ist, die Umfrage löschen
        poll.delete()
        # Nach dem Löschen zur 'group'-Ansicht zurückkehren (Pfad anpassen, wenn nötig)
        return HttpResponseRedirect(reverse('group_detail', kwargs={'group_id': group_id}))  
        # 'group' ist der Name der Ansicht, zu der du nach dem Löschen der Umfrage zurückkehren möchtest

    # Falls das Formular nicht gesendet wurde, render die Seite normal (hier könnte man auch eine Fehlermeldung anzeigen)
    return render(request, 'group.html', {'poll': poll})


