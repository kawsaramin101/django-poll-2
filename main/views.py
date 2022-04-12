from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from ipware import get_client_ip 
from django.contrib import messages

from .models import Choice, Question, Voter, Vote


def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.MultipleObjectsReturned as e:
        print('ERR====>', e)
    except classmodel.DoesNotExist:
        return None


def index(request):
    context = {}
    if request.user.is_authenticated:
        user_polls = Question.objects.filter(creator=request.user)
        context["user_polls"] = user_polls
    #latest_question_list = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    #context = {'latest_question_list': latest_question_list}
    return render(request, 'main/index/index.html', context)
    
    
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {
        'question': question,
    }
    client_ip, is_routable = get_client_ip(request)
    if request.user.is_authenticated:
        voter = get_or_none(Voter,ip_address=client_ip, user=request.user)
    else:
        voter = get_or_none(Voter,ip_address=client_ip)

    if voter is not None and voter in question.voters.all():
        if question.vote_changeable:
            for choice in question.choices.all():
                if voter in choice.voters.all():
                    context["selected_choice"] = choice.id
                    break
            return render(request, 'main/detail/detail.html', context)
        else:
            messages.info(request, "You have already voted and this vote can not be changed")
            return redirect(f"/{question.id}/results/")
   
    return render(request, 'main/detail/detail.html', {'question': question})
    
    
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    #print(question.choices.get(id=2).voters.all().count())
    return render(request, 'main/results.html', {'question': question})
    

def vote(request, question_id):
    client_ip, is_routable = get_client_ip(request)
    if client_ip is None:
        pass
    else:
        if request.user.is_authenticated:
            voter, created = Voter.objects.get_or_create(ip_address=client_ip, user=request.user)
        else:
            voter, created = Voter.objects.get_or_create(ip_address=client_ip)
        question = get_object_or_404(Question, pk=question_id)
        try:
            selected_choice = question.choices.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            return render(request, 'main/detail/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
            })
        else:
            if not voter in question.voters.all() and question.vote_changeable:
                try:
                    Vote.objects.create(choice=selected_choice, voter=voter)
                except IntegrityError:
                    messages.error(request, "You have already voted and this vote can not be changed")
                    return render(request)
            else:
                messages.info(request, "You have already voted and this vote can not be changed")
                response = HttpResponse()
                response.headers['HX-Redirect'] = f"/{question.id}/results/"
                return response
        return HttpResponseRedirect(reverse('main:results', args=(question.id,)))
    return HttpResponse("Could not resolve your id")