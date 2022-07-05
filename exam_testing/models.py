from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from itertools import chain


class User(AbstractUser):
    secret_question = models.TextField(default=None, blank=True, null=True)
    secret_question_answer = models.TextField(default=None, blank=True, null=True)

    def generate_test_questions(self):
        questions = list(chain(QuestionUser.objects.filter(user=self, done=0).order_by('?')[:6],
                               QuestionUser.objects.filter(user=self, done=1).order_by('?')[:2],
                               QuestionUser.objects.filter(user=self, done=2).order_by('?')[:1],
                               ))
        test = Test.objects.create(user=self, num=Test.objects.filter(user=self).count())
        result = []
        for question_user in questions:
            question = question_user.question
            test.questions.add(question)
            result.append((question, question.get_answers()))
        test.save()
        return test.num, result

    def progress(self):
        done_all_quests = len(QuestionUser.objects.filter(done=2))
        progr = int(done_all_quests/len(Question.objects.all())) * 100
        return progr

    def all_user_tests(self):
        return list(Test.objects.filter(user=self).ordered_by('-id'))

class Question(models.Model):
    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'

    title = models.CharField(max_length=100, default='Вопрос', verbose_name='Заголовок')
    text = models.TextField(verbose_name="Текст вопроса")

    def save(self, *args, **kwargs):
        super(Question, self).save(*args, **kwargs)
        for user in User.objects.all():
            QuestionUser(question=self, user=user).save()

    def get_answers(self):
        return tuple(QuestionAnswer.objects.filter(question=self))

    def __str__(self):
        return self.title


class QuestionUser(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    done = models.IntegerField(default=0)  # 0 - не пройден(неверный), 1 - частично верно, 2 - верно


class QuestionAnswer(models.Model):  # ответ на каждый чекбокс
    text = models.TextField(verbose_name='Текст варианта ответа')
    correct = models.BooleanField(verbose_name='Правильный ответ?')
    question = models.ForeignKey("Question", on_delete=models.CASCADE)

    def __str__(self):
        return 'Вариант ответа'


class UserAttempt(models.Model):
    class Meta:
        verbose_name = 'Пройденный тест'
        verbose_name_plural = 'Пройденные тесты'

    test = models.ForeignKey('Test', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    question_answer = models.ForeignKey('QuestionAnswer', on_delete=models.CASCADE)


class Test(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    finish_date = models.DateTimeField(auto_now_add=True)
    num = models.IntegerField()
    questions = models.ManyToManyField(Question)

    @classmethod
    def get_last_tests(cls, count=15):
        return list(Test.objects.order_by('-finish_date')[:count])

    def count_of_done(self):
        cnt = 0
        for quest in self.questions.objects:
            first = set(QuestionAnswer.objects.filter(question=quest, correct=True))
            second = set(map(lambda x: x.question_answer, UserAttempt.objects.filter(test=self, question=quest)))
            if len(first ^ second) == 0:
                cnt += 1
        return cnt

    def questions_count(self):
        return len(self.questions)

