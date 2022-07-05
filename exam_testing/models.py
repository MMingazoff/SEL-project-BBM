from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    secret_question = models.TextField(default=None, blank=True, null=True)
    secret_question_answer = models.TextField(default=None, blank=True, null=True)


class Question(models.Model):
    text = models.TextField()


class QuestionAnswer(models.Model):  # ответ на каждый чекбокс
    text = models.TextField()
    correct = models.BooleanField()
    question = models.ForeignKey("Question", on_delete=models.CASCADE)


class UserAttempt(models.Model):
    test = models.ForeignKey('Test', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    question_answer = models.ForeignKey('QuestionAnswer', on_delete=models.CASCADE)


class Test(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    finish_date = models.DateTimeField(auto_now_add=True)
    num = models.IntegerField()

    def get_last_tests(self, count=15):
        return list(Test.objects.order_by('-finish_date')[:count])

    def count_of_done(self):
        cnt = 0
        for tst_qst in TestQuestions.objects.filter(test=self):
            first = QuestionAnswer.objects.filter(question=tst_qst.question, correct=True).filter()
            second = list(map(lambda x: x.question, UserAttempt.objects.filter(test=self, question=tst_qst.question)))
            if first == second:  # а это работает?
                cnt += 1


class TestQuestions(models.Model):
    test = models.ForeignKey('Test', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
