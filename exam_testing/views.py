from django.shortcuts import render
from .models import UserAttempt, Question, TestQuestions

def headpage(request):
    list_attempts = []
    for att in UserAttempt.objects.all():
        us_name = att.test.user.username
        tst_nm = att.test.num
        qsts_done = len(...)
        qsts_cnt = len(TestQuestions.objects.filter(test=att.test))
        progr = ...
        data = att.test.finish_date

    return render(request, 'exam_testing/headpage.html')