from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login, logout
from .models import User, Test, QuestionAnswer, Question, UserAttempt
import os

templates_path = os.path.abspath(__file__)[:-8] + 'templates/exam_testing/'


def main_page(request):
    return HttpResponse('Main page')


def test(request):
    return HttpResponse('Testing page')


def test_results(request):
    return HttpResponse('Test results')


def headpage(request):
    if not request.user.is_authenticated:
        return render(request, templates_path+'headpage_anon.html')

    username = request.user.username
    last_tests = Test.get_last_tests()
    self_progr = request.user.progress()
    user_tests = request.user.all_user_tests()


    return render(request, templates_path+'headpage.html', context={'list_elems': list_attempts,
                                                                    'self_progr': self_progr,
                                                                    'list_of_user_tests': list_of_user_tests,
                                                                    'request': request})


def register(request):
    if request.method == 'GET':
        return render(request, templates_path + 'register.html')
    if request.method == 'POST':
        if not User.objects.filter(username=request.POST.get('login')).exists():
            if request.POST.get('password') != request.POST.get('password_two'):
                return render(request, templates_path + 'register.html', {'error': 'Пароли не совпадают'})
            user = User.objects.create_user(username=request.POST.get('login'),
                                            password=request.POST.get('password'),
                                            secret_question=request.POST.get('secret_question'),
                                            secret_question_answer=make_password(request.POST.get('secret_question_answer'))
                                            )
        else:
            return render(request, templates_path + 'register.html', {'error': 'Такое имя пользователя занято'})
        user.save()
        return redirect('/login/')


def user_logout(request):
    logout(request)
    return redirect("/")


def user_login(request):
    if request.method == 'GET':
        return render(request, templates_path + 'login.html')
    if request.method == 'POST':
        if User.objects.filter(username=request.POST.get('login')).exists():
            user = User.objects.get(username=request.POST.get('login'))
        else:
            return render(request, templates_path + 'login.html', {'error': 'Такого пользователя не существует'})
        if user.check_password(request.POST.get('password')):
            login(request, user)
            return redirect('/')
        else:
            return render(request, templates_path + 'login.html', {'error': 'Неверный пароль'})


def recover_password(request):
    if request.method == 'GET':
        if request.GET.get('login'):
            if User.objects.filter(username=request.GET.get('login')).exists():
                user = User.objects.get(username=request.GET.get('login'))
                return render(request, templates_path + 'password_recovery.html', {'secret_question': user.secret_question, 'login': request.GET.get('login')})
            else:
                return render(request, templates_path + 'password_recovery_startpage.html', {'error': 'Такого пользователя не существует'})
        else:
            return render(request, templates_path + 'password_recovery_startpage.html')
    if request.method == 'POST':
        user = User.objects.get(username=request.POST.get('login'))
        if check_password(request.POST.get('secret_question_answer'), user.secret_question_answer):
            if request.POST.get('password') != request.POST.get('password_two'):
                return render(request, templates_path + 'password_recovery.html', {'secret_question': user.secret_question,
                                                                                   'error': 'Пароли не совпадают',
                                                                                   'login': request.POST.get('login')})
            else:
                user.set_password(request.POST.get('password'))
                user.save()
                return redirect('/login/')
        else:
            return render(request, templates_path + 'password_recovery.html', {'secret_question': user.secret_question,
                                                                               'error': 'Ответ на контрольный вопрос неверный',
                                                                               'login': request.POST.get('login')})
