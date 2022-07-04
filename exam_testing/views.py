from django.shortcuts import render
from .models import *
import os

templates_path = os.path.abspath(__file__)[:-8] + 'templates/exam_testing/'

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
    username = request.POST.get('username')
    self_progr = None
    list_of_user_tests = []
    if username is not None:
        usr = User.objects.get(username=username)
        user_tests = list(Test.objects.filter(user=usr))
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
        done_qsts2 = dict()
        for qst in Question.objects.all():
            done_qsts2[qst] = False
        for ot_test in Test.objects.filter(user=usr).order_by('id'):
            for test_quest in TestQuestions.objects.filter(test=ot_test):
                left = QuestionAnswer.objects.filter(question=test_quest.question, correct=True)
                right = list(map(lambda x: x.question, UserAttempt.objects.filter(test=ot_test, question=test_quest.question)))
                if left == right:
                    done_qsts2[test_quest.question] = True
                else:
                    done_qsts2[test_quest.question] = False
        self_progr = len(list(filter(lambda x: x == True, done_qsts2.values())))

    return render(request, templates_path+'headpage.html', context={'list_elems': list_attempts, 'username': username,
                                                                  'self_progr': self_progr, 'list_of_user_tests': list_of_user_tests})
