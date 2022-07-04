from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from .models import Question
from django.db.utils import IntegrityError

import os

templates_path = os.path.abspath(__file__)[:-8] + 'templates/exam_testing/'

def main_page(request):
    return HttpResponse('Main page')


def test(request):
    return HttpResponse('Testing page')


def test_results(request):
    questions = Question.objects.all()
    dict_of_questions = {}
    i=1
    for question in questions:
        dict_of_questions[f"question{i}"] = question.text
        i+=1
    return render(request, templates_path + 'results.html',dict_of_questions)

