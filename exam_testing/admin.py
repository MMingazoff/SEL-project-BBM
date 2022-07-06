from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Question, QuestionAnswer, UserAttempt, User, QuestionUser
from django.forms import TextInput, Textarea
from django.db import models


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_staff')


class QuestionAnswerInline(admin.TabularInline):
    model = QuestionAnswer
    verbose_name = 'вариант ответа'
    verbose_name_plural = 'варианты ответов'
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 50})},
    }


class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        QuestionAnswerInline,
    ]
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }


admin.site.register(User, UserAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(UserAttempt)
admin.site.register(QuestionUser)
admin.site.unregister(Group)
