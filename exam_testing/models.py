from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

class User(AbstractUser):
    secret_question = models.IntegerField(default=0, blank=True, null=True)
    secret_question_answer = models.CharField(max_length=100, default=None, blank=True, null=True)

class Question(models.Model):
    text = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    
class QuestionAnswer(models.Model): # ответ на каждый чекбокс
    text = models.TextField()
    correct = models.BooleanField()
    question = models.ForeignKey("Question", on_delete = models.CASCADE)
    
class UserAttempt(models.Model):
    test = models.ForeignKey('Test', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    question_answer = models.ForeignKey('QuestionAnswer', on_delete=models.CASCADE)
    
class Test(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    finish_date = models.DateTimeField(auto_now_add=True)
    num = models.IntegerField()
    
class TestQuestions(models.Model):
    test = models.ForeignKey('Test', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    