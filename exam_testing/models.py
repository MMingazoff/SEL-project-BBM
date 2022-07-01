from django.conf import settings
from django.db import models



class Question(models.Model):
    text = models.TextField()
    
class QuestionAnswer():
    text = models.TextField()
    correct = models.BooleanField()
    question = models.ForeignKey("Question", on_delete = models.CASCADE)
    
class UserAttempt(models.Model):
    test = models.ForeignKey('Test', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    question_answer = models.ForeignKey('QuestionAnswer', on_delete=models.CASCADE)
    
class Test(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    finish_date = models.DateField(auto_now_add=True)
    num = models.IntegerField()
    
class TestQuestions(models.Model):
    test = models.ForeignKey('Test', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    