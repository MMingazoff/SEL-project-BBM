from django.contrib import admin
from .models import Question, QuestionAnswer, TestQuestions, Test, UserAttempt, User, QuestionUser

admin.site.register(Question)
admin.site.register(QuestionAnswer)
admin.site.register(TestQuestions)
admin.site.register(Test)
admin.site.register(UserAttempt)
admin.site.register(User)
admin.site.register(QuestionUser)
