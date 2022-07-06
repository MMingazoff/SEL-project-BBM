from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login, logout
from .models import User, Test, TestQuestions, QuestionAnswer, Question, UserAttempt
import os
import random


templates_path = os.path.abspath(__file__)[:-8] + 'templates/exam_testing/'


def main_page(request):
    return HttpResponse('Main page')


def test(request):
    n = 9  # QUESTION_NUM
    questions = Question.objects.all()
    questions = random.shuffle(questions)
    questions = questions[0:n]
    list_of_answers = {}
    i=1
    for question in questions:
        answers_list = QuestionAnswer.objects.filter( question = question)
        list_of_answers.append(answers_list)
        i+=1
    
    return render(request, templates_path+"test.html", context={"questions": questions,"list_of_answer": list_of_answers})

def test_results(request):
    return HttpResponse('Test results')


def headpage(request):
    list_attempts = []
    for test in Test.objects.order_by("-id")[0:15]:
        us_name = test.user.username
        tst_nm = test.num
        cnt = 0
        for tst_qst in TestQuestions.objects.filter(test=test):
            first = QuestionAnswer.objects.filter(question=tst_qst.question, correct=True)
            second = list(map(lambda x: x.question, UserAttempt.objects.filter(test=test, question=tst_qst.question)))
            if first == second: # а это работает?
                cnt += 1
        done_qsts = dict()
        for qst in Question.objects.all():
            done_qsts[qst] = False
        for ot_test in Test.objects.filter(user=test.user).order_by('id'):
            for test_quest in TestQuestions.objects.filter(test=ot_test):
                left = QuestionAnswer.objects.filter(question=test_quest.question, correct=True)
                right = list(map(lambda x: x.question, UserAttempt.objects.filter(test=ot_test, question=test_quest.question)))
                if left == right:
                    done_qsts[test_quest.question] = True
                else:
                    done_qsts[test_quest.question] = False
        done_all_quests = len(list(filter(lambda x: x == True, done_qsts.values())))
        qsts_done = cnt
        qsts_cnt = len(TestQuestions.objects.filter(test=test))
        progr = int(done_all_quests/len(Question.objects.all())) * 100
        date = test.finish_date
        list_attempts.append([us_name, tst_nm, qsts_done, qsts_cnt, progr, date])
    user = request.user
    self_progr = None
    list_of_user_tests = []
    if not user.is_anonymous:
        user_tests = list(Test.objects.filter(user=user))
        takes = []
        for test_2 in user_tests:
            takes.append(test_2.num)
            done2 = 0
            for tst_qst in TestQuestions.objects.filter(test=test_2):
                first = QuestionAnswer.objects.filter(question=tst_qst.question, correct=True)
                second = list(map(lambda x: x.question, UserAttempt.objects.filter(test=test_2, question=tst_qst.question)))
                if first == second: # а это работает?
                    done2 += 1
            takes.append(done2)
            takes.append(len(TestQuestions.objects.filter(test=test_2)))
            takes.append(test_2.finish_date)
            list_of_user_tests.append(takes)
        done_qsts2 = dict()
        for qst in Question.objects.all():
            done_qsts2[qst] = False
        for ot_test in Test.objects.filter(user=user).order_by('id'):
            for test_quest in TestQuestions.objects.filter(test=ot_test):
                left = QuestionAnswer.objects.filter(question=test_quest.question, correct=True)
                right = list(map(lambda x: x.question, UserAttempt.objects.filter(test=ot_test, question=test_quest.question)))
                if left == right:
                    done_qsts2[test_quest.question] = True
                else:
                    done_qsts2[test_quest.question] = False
        self_progr = len(list(filter(lambda x: x == True, done_qsts2.values())))

    return render(request, templates_path+'headpage.html', context={'list_elems': list_attempts,
                                                                    'self_progr': self_progr,
                                                                    'list_of_user_tests': list_of_user_tests,
                                                                    'request': request})
'''
def test(request):
    questions = Question.objects.all()
    dict_of_questions_answers = {}
    dict_of_questions = {}
    q=1
    for question in questions:
        small_dict_of_question = {}
        answers_list = QuestionAnswer.objects.filter( question = question)
        q1= 1
        for answer in answers_list:
            small_dict_of_question[f'question_answer{q1}'] = answer.text
            q+=1
        dict_of_questions[f'question{q}'] = question.text
        dict_of_questions_answers[f'question{q}'] = small_dict_of_question
        q+=1
    return render(request, templates_path+'test.html', context = {'dict_of_question': dict_of_questions, 'dict_of_questions_answers' : dict_of_questions_answers})
'''
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