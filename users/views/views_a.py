import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.forms.models import model_to_dict

from ..forms import CreateQuestionForm, EditQuestionForm
from main.models import Question

@login_required
def create_poll(request):
    return render(request, 'users/create-poll.html')
    
    
@login_required
def create_question(request):
    if request.method == "POST":
        form = CreateQuestionForm(request.POST or None)
        if form.is_valid():
            question = form.save(commit=False)
            question.creator = request.user
            question.save()
            messages.success(request, "Question created successfully")
            response = HttpResponse()
            response.headers['HX-Redirect'] = f"/edit_question/{question.id}"
            return response
        else:
            return HttpResponse(f'{form.errors}')
    else:
        HttpResponse("Method Not allowed")


@login_required
def edit_question(request, id):
    question = get_object_or_404(Question, id=id)
    #if request.user == question.creator:
    if request.method == "GET":
        pass
        #return render(request, 'users/partials/')
    elif request.method == "PATCH":
        #question = get_object_or_404(Question, id=id)
        form = EditQuestionForm(request.POST, instance=question)
        #else:
            #raise PermissionDenied("You are not permitted to edit this question")
        if form.is_valid():
            form.save()
            return HttpResponse("<p class='has-text-success'>Question changed successfully</p>")
        else:
            return HttpResponse(f'{form.errors}')
            