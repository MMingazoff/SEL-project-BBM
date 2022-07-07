from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from itertools import chain
from random import shuffle
from typing import Tuple


class User(AbstractUser):
    secret_question = models.TextField(default=None, blank=True, null=True)
    secret_question_answer = models.TextField(default=None, blank=True, null=True)

    def generate_test_questions(self):
        """
        Генерация 9 случайных вопросов.
        :return: номер теста, список кортежей с вопросом и кортежом вариантов ответов на вопрос
        """
        incorrect = QuestionUser.objects.filter(user=self, done=0)
        half_correct = QuestionUser.objects.filter(user=self, done=1)
        correct = QuestionUser.objects.filter(user=self, done=2)
        incorrect_num, half_correct_num, correct_num = User._calculate_questions_num(incorrect.count(),
                                                                                     half_correct.count(),
                                                                                     correct.count())
        questions = list(chain(incorrect.order_by('?')[:incorrect_num],  # неверные
                               half_correct.order_by('?')[:half_correct_num],  # частичные
                               correct.order_by('?')[:correct_num],  # верные
                               ))
        shuffle(questions)
        test = Test.objects.create(user=self, num=Test.objects.filter(user=self).count())
        result = []
        for question_user in questions:
            question = question_user.question
            test.questions.add(question)
            result.append((question, question.get_answers()))
        test.save()
        return test.num, result

    @staticmethod
    def _calculate_questions_num(incorrect: int, half_correct: int, correct: int) -> Tuple[int, int, int]:
        """Происходит расчет какое количество вопросов каждого типа (верные, частично верные, неверные) будет в тесте"""
        incorrect_left, half_correct_left, correct_left = incorrect, half_correct, correct
        incorrect_num, half_correct_num, correct_num = 0, 0, 0
        # всего 9 вопросов -> 9 слотов (по слоту на вопрос)
        for pos in range(6):  # слоты потенциально на неверные
            if incorrect_left > 0:  # есть неверные, значит берем
                incorrect_num += 1
                incorrect_left -= 1
            elif half_correct_left > 0:  # неверные закончились, значит берем частичные
                half_correct_num += 1
                half_correct_left -= 1
            else:  # неверные и частичные закончились, значит берем верные
                delta = 6 - incorrect_num - half_correct_num
                correct_left -= delta
                correct_num += delta
                break
        for pos in range(6, 8):  # слоты потенциально на частичные
            if half_correct_left > 0:  # есть частичные, значит берем
                half_correct_num += 1
                half_correct_left -= 1
            elif incorrect_left > 0:  # частичные закончились, значит берем неверные
                incorrect_num += 1
                incorrect_left -= 1
            else:  # частичные и неверные закончились, значит берем верные
                correct_left -= 1
                correct_num += 1
        if correct_left > 0:
            correct_num += 1
        elif incorrect_left > 0:  # есть неверные, значит берем
            incorrect_num += 1
        elif half_correct_left > 0:  # неверные закончились, значит берем частичные
            half_correct_num += 1
        return incorrect_num, half_correct_num, correct_num

    def on_register(self):
        """Создает вопросы при регистрации пользователя (для проверки степени пройденности)"""
        QuestionUser.objects.bulk_create([QuestionUser(question=question, user=self) for question in Question.objects.all()])


class Question(models.Model):
    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'

    title = models.CharField(max_length=100, default='Вопрос', verbose_name='Заголовок')
    text = models.TextField(verbose_name="Текст вопроса")

    def save(self, *args, **kwargs):
        """
        Сохраняя вопрос, создаем у каждого пользователя строку с указанием на вопрос.
        Сделано, чтобы знать пройден вопрос или нет
        """
        super(Question, self).save(*args, **kwargs)
        for user in User.objects.all():
            QuestionUser(question=self, user=user).save()

    def get_answers(self):
        """Варианты ответа на вопрос"""
        return tuple(QuestionAnswer.objects.filter(question=self))

    def __str__(self):
        return self.title


class QuestionUser(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    done = models.IntegerField(default=0)  # 0 - не пройден(неверный), 1 - частично верно, 2 - верно


class QuestionAnswer(models.Model):  # ответ на каждый чекбокс
    text = models.TextField()
    correct = models.BooleanField()
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
