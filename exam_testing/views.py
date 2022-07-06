from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login, logout
from .models import User, Test, QuestionAnswer, Question, UserAttempt


def main_page(request):
    return HttpResponse('Main page')


def test_results(request):
    return HttpResponse('Test results')


def headpage_non_auth(request):
    return render(request, 'exam_testing/headpage_anon.html')


@login_required(login_url='non_auth/')
def headpage(request):
    username = request.user.username
    last_tests = Test.get_last_tests()
    self_progr = request.user.progress()
    user_tests = request.user.all_user_tests()

    return render(request, 'exam_testing/headpage.html', context={'username': username, 'last_tests': last_tests,
                                                                    'self_progr': self_progr, 'user_tests': user_tests})
def make_test(request):
    """Рендер страницы с тестом"""
    test_num, test_questions = User.generate_test_questions(request.user)
    test_questions = list(enumerate(test_questions, 1))
    test_questions = [(num, question, question_answers) for num, (question, question_answers) in test_questions]
    return render(request, 'exam_testing/test.html', {'test_questions': test_questions,
                                                      'test_num': test_num,
                                                      })


def register(request):
    if request.method == 'GET':
        return render(request, 'exam_testing/register.html')
    if request.method == 'POST':
        if not User.objects.filter(username=request.POST.get('login')).exists():
            if request.POST.get('password') != request.POST.get('password_two'):
                return render(request, 'exam_testing/register.html', {'error': 'Пароли не совпадают'})
            user = User.objects.create_user(username=request.POST.get('login'),
                                            password=request.POST.get('password'),
                                            secret_question=request.POST.get('secret_question'),
                                            secret_question_answer=make_password(
                                                request.POST.get('secret_question_answer'))
                                            )
        else:
            return render(request, 'exam_testing/register.html', {'error': 'Такое имя пользователя занято'})
        user.save()
        return redirect('/login/')


def user_logout(request):
    logout(request)
    return redirect("/")


def user_login(request):
    if request.method == 'GET':
        return render(request, 'exam_testing/login.html')
    if request.method == 'POST':
        if User.objects.filter(username=request.POST.get('login')).exists():
            user = User.objects.get(username=request.POST.get('login'))
        else:
            return render(request, 'exam_testing/login.html', {'error': 'Такого пользователя не существует'})
        if user.check_password(request.POST.get('password')):
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'exam_testing/login.html', {'error': 'Неверный пароль'})


def recover_password(request):
    if request.method == 'GET':
        if request.GET.get('login'):
            if User.objects.filter(username=request.GET.get('login')).exists():
                user = User.objects.get(username=request.GET.get('login'))
                return render(request, 'exam_testing/password_recovery.html',
                              {'secret_question': user.secret_question, 'login': request.GET.get('login')})
            else:
                return render(request, 'exam_testing/password_recovery_startpage.html',
                              {'error': 'Такого пользователя не существует'})
        else:
            return render(request, 'exam_testing/password_recovery_startpage.html')
    if request.method == 'POST':
        user = User.objects.get(username=request.POST.get('login'))
        if check_password(request.POST.get('secret_question_answer'), user.secret_question_answer):
            if request.POST.get('password') != request.POST.get('password_two'):
                return render(request, 'exam_testing/password_recovery.html',
                              {'secret_question': user.secret_question,
                               'error': 'Пароли не совпадают',
                               'login': request.POST.get('login')})
            else:
                user.set_password(request.POST.get('password'))
                user.save()
                return redirect('/login/')
        else:
            return render(request, 'exam_testing/password_recovery.html', {'secret_question': user.secret_question,
                                                                           'error': 'Ответ на контрольный вопрос неверный',
                                                                           'login': request.POST.get('login')})
