from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from itertools import chain
from random import random, Random, randint, shuffle
from typing import Tuple


class User(AbstractUser):
    secret_question = models.TextField(default=None, blank=True, null=True)
    secret_question_answer = models.TextField(default=None, blank=True, null=True)

    def generate_test_questions(self):
        """
        Генерация 9 случайных вопросов.
        :return: Номер теста, список кортежей с вопросом и кортежом вариантов ответов на вопрос
        """

        # Если пользователь сгенерировал себе тест, но еще не прошел его, то новый тест генерироваться не должен
        last_test = Test.objects.filter(user=self, completed=False)
        if last_test.exists():
            return last_test.first().get_test_questions()

        questions_pool = QuestionUser.objects.filter(user=self, question__active=True)
        incorrect = questions_pool.filter(done=0)
        half_correct = questions_pool.filter(done=1)
        correct = questions_pool.filter(done=2)
        incorrect_num, half_correct_num, correct_num = User._calculate_questions_num(incorrect.count(),
                                                                                     half_correct.count(),
                                                                                     correct.count())
        questions = list(chain(incorrect.order_by('?')[:incorrect_num],  # неверные
                               half_correct.order_by('?')[:half_correct_num],  # частичные
                               correct.order_by('?')[:correct_num],  # верные
                               ))
        seed = randint(0, 1000)
        test = Test.objects.create(user=self, num=Test.objects.filter(user=self).count() + 1, seed=seed)
        result = []
        for question_user in questions:
            question = question_user.question
            test.questions.add(question)
        questions = list(test.questions.all())
        Random(seed).shuffle(questions)
        for question in questions:
            question_answers = question.get_answers()
            shuffle(question_answers)
            result.append((question, question_answers))
        test.save()
        return test, result

    def has_unsubmitted_test(self):
        """Проверка на то, есть ли не пройденный тест"""
        return Test.objects.filter(user=self, completed=False).exists()

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
        # слот потенциально на верный
        if correct_left > 0:  # есть верный, берем
            if incorrect_left > 0:  # если есть неверный, то с вероятностью 45% он будет на последнем слоте
                if random() >= 0.55:
                    correct_num += 1
                else:
                    incorrect_num += 1
            else:  # неверного нет, значит просто берем верный
                correct_num += 1
        elif incorrect_left > 0:  # нет верного, но есть неверные, значит берем
            incorrect_num += 1
        elif half_correct_left > 0:  # неверные закончились, значит берем частичные
            half_correct_num += 1
        return incorrect_num, half_correct_num, correct_num

    def on_register(self):
        """Создает вопросы при регистрации пользователя (для проверки степени пройденности)"""
        QuestionUser.objects.bulk_create([QuestionUser(question=question, user=self) for question in Question.objects.all()])

    def progress(self):
        done_quests = QuestionUser.objects.filter(user=self, done=2).count()
        all_questions = Question.objects.filter(active=True).count() or 1
        progr = int((done_quests / all_questions) * 100)
        return progr

    def all_user_tests(self):
        return list(Test.objects.filter(user=self, completed=True).order_by('-start_date'))


class Question(models.Model):
    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'

    title = models.CharField(max_length=100, default='Вопрос', verbose_name='Заголовок')
    text = models.TextField(verbose_name="Текст вопроса")
    active = models.BooleanField(default=True, verbose_name='Активный')

    def save(self, *args, **kwargs):
        """
        Сохраняя вопрос, создаем у каждого пользователя строку с указанием на вопрос.
        Сделано, чтобы знать пройден вопрос или нет
        """
        super(Question, self).save(*args, **kwargs)
        if not QuestionUser.objects.filter(question=self).exists():
            for user in User.objects.all():
                QuestionUser(question=self, user=user).save()

    def get_answers(self):
        """Варианты ответа на вопрос"""
        return list(QuestionAnswer.objects.filter(question=self))

    def correct_answers(self, test):
        cnt = 0
        count_of_correct = QuestionAnswer.objects.filter(question=self, correct=True).count()
        if count_of_correct == 0:
            return 0
        user_answers = list(
            map(lambda x: x.question_answer,
                UserAttempt.objects.filter(test=test, question=self)))
        for answer in QuestionAnswer.objects.filter(question=self):
            if answer.correct and answer in user_answers:
                cnt += 1
            elif answer.correct and answer not in user_answers:
                cnt -= 1
            elif not answer.correct and answer in user_answers:
                cnt -= 1
        res = cnt / count_of_correct
        if res == 1:
            return 2  # верно
        elif res >= 0.5:
            return 1  # частично верно
        elif res < 0.5:
            return 0  # верно

    def __str__(self):
        return self.title


class QuestionUser(models.Model):
    class Meta:
        verbose_name = 'Степень пройденности каждого вопроса'
        verbose_name_plural = 'Степени пройденности каждого вопроса'
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    done = models.IntegerField(default=0)  # 0 - не пройден(неверный), 1 - частично верно, 2 - верно


class QuestionAnswer(models.Model):  # ответ на каждый чекбокс
    class Meta:
        verbose_name = 'Ответ на вопрос'
        verbose_name_plural = 'Ответы на вопросы'
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
    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    num = models.IntegerField()
    questions = models.ManyToManyField(Question)
    seed = models.IntegerField()
    progress = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)

    @classmethod
    def get_last_tests(cls, count=15):
        return list(Test.objects.filter(completed=True).order_by('-start_date')[:count])

    def get_test_questions(self):
        """Получить вопросы с не пройденного теста"""
        result = []
        for question in self.questions.all():
            result.append((question, question.get_answers()))
        return self, result

    def count_of_done(self):
        cnt = 0
        for quest in self.questions.all():
            first = set(QuestionAnswer.objects.filter(question=quest, correct=True))
            second = set(map(lambda x: x.question_answer, UserAttempt.objects.filter(test=self, question=quest)))
            if len(first ^ second) == 0:
                cnt += 1
        return cnt

    def get_results(self, user) -> list:
        if user.has_unsubmitted_test():
            return []
        result = list()
        questions = list(self.questions.all())
        Random(self.seed).shuffle(questions)
        for num, question in enumerate(questions, 1):
            result.append((num, question.text, question.correct_answers(self)))
        return result

    def set_results(self):
        """Изменяет степень пройденности в зависимости от результата"""
        for question in self.questions.all():
            qu = QuestionUser.objects.get(user=self.user, question=question)
            qu.done = question.correct_answers(self)
            qu.save()
        self.progress = int((QuestionUser.objects.filter(user=self.user, done=2, question__active=True).count()
                             / Question.objects.count()) * 100)
        self.completed = True
        self.save()


def set_data(request):
    """Фиксирует попытку/ответ пользователя на тест в базе данных"""
    test = Test.objects.get(id=int(request.POST.get("test_id")))
    for question_id in request.POST:
        if question_id.startswith("q_"):
            for answer_id in request.POST.getlist(question_id):
                UserAttempt(test=test,
                            question=Question.objects.get(id=int(question_id[2:-2])),
                            question_answer=QuestionAnswer.objects.get(id=int(answer_id[7:]))
                            ).save()
    test.set_results()
