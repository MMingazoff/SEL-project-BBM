import sqlite3
import sys

sql_script = """
INSERT INTO exam_testing_question (id, title, text, active)
VALUES (1, 'Абстракция и аппликация', 'Что такое аппликация и абстракция?', 1);

INSERT INTO exam_testing_question (id, title, text, active)
VALUES (2, 'Каррирование', 'При каррировании ...', 1);

INSERT INTO exam_testing_question (id, title, text, active)
VALUES (3, 'LISP', 'Какие из данных выражений на языке LISP возвращают хвост списка длиной 3?', 1);

INSERT INTO exam_testing_question (id, title, text, active)
VALUES (4, 'Неизменяемые типы', 'Что относится к неизменяемым типам в Python?', 1);

INSERT INTO exam_testing_question (id, title, text, active)
VALUES (5, 'Объединить 2 множества', 'Как объединить два множества(set) a и b?', 1);

INSERT INTO exam_testing_question (id, title, text, active)
VALUES (6, 'LIFO', 'Что поддерживает правило LIFO?', 1);

INSERT INTO exam_testing_question (id, title, text, active)
VALUES (7, 'Текстовые файлы', 'Выберите расширения текстовых файлов:', 1);

INSERT INTO exam_testing_question (id, title, text, active)
VALUES (8, 'Потоки ввода вывода', 'Какие виды потоков ввода вывода есть в Python?', 1);

INSERT INTO exam_testing_question (id, title, text, active)
VALUES (9, 'Флаги в open', 'Выберите верные утверждения про флаги для открытия файлов:', 1);

INSERT INTO exam_testing_question (id, title, text, active)
VALUES (10, 'run у Thread', 'В чем заключается смысл метода run у потока:', 1);

INSERT INTO exam_testing_question (id, title, text, active)
VALUES (11, 'Lock', 'Какие методы есть у класса Lock, и что они делают?', 1);

INSERT INTO exam_testing_question (id, title, text, active)
VALUES (12, 'Рефлексия', 'Какие варианты вызовут у экземпляра класса X метод Y, если X, Y - строки?', 1);

INSERT INTO exam_testing_question (id, title, text, active)
VALUES (13, 'get/set/hasattr', 'Выберите верные утверждения:', 1);

INSERT INTO exam_testing_question (id, title, text, active)
VALUES (14, 'Рефлексия 2', 'Рефлексия про ... :', 1);

INSERT INTO exam_testing_question (id, title, text, active)
VALUES (15, 'Синхронизация', 'Что позволяет делать синхронизация потоков в Python?', 1);

INSERT INTO exam_testing_question (id, title, text, active)
VALUES (16, 'Random Access File', 'Как открыть Random Access File в Python?', 1);

INSERT INTO exam_testing_question (id, title, text, active)
VALUES (17, 'Random Access File методы', 'Какие методы есть у файла с произвольным доступом', 1);

INSERT INTO exam_testing_question (id, title, text, active)
VALUES (18, 'Цикл жизни модульного тестирования', 'Что относится к жизненному циклу модульного тестирования?', 1);

INSERT INTO exam_testing_question (id, title, text, active)
VALUES (19, 'Срезы', 'Что справедливо для данного кода mylist[:0:1], где mylist - не пустой список?', 1);

INSERT INTO exam_testing_question (id, title, text, active)
VALUES (20, 'Индексация коллекций', 'Какие коллекции индексируемы?', 1);

INSERT INTO exam_testing_question (id, title, text, active)
VALUES (21, 'Модуль', 'Что такое модуль?', 1);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (1, 'Аппликация - объявление функции, абстракция - применение функции к аргументам', 0, 1);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (2, 'Аппликация -  применение функции к аргументам, Абстракция - объявление функции', 0, 1);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (3, 'Абстракция - применение функции к аргументу, аппликация - декларирование функции', 0, 1);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (4, 'Абстракция -  декларирование функции, аппликация - применение функции к аргументу', 1, 1);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (5, 'Функции одноместные', 1, 2);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (6, '(Промежуточным) результатом может быть функция от одного аргумента', 1, 2);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (7, '(Промежуточным) результатом может быть фунцкия от нескольких аргументов', 0, 2);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (8, 'Результатом может быть конкретное значение', 1, 2);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (9, '(car (1 2 3 4))', 0, 3);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (10, '(cdr (5 3 2 6))', 1, 3);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (11, '(cdr (5 3 2 6))', 0, 3);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (12, '(cdr (1 2 3 4))', 1, 3);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (13, 'list', 0, 4);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (14, 'tuple', 1, 4);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (15, 'string', 1, 4);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (16, 'set', 0, 4);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (17, 'frozenset', 1, 4);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (18, 'dict keys', 1, 4);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (19, 'dict values', 0, 4);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (20, 'a | b', 1, 5);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (21, 'a & b', 0, 5);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (22, 'a ^ b', 0, 5);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (23, 'a.union(b)', 1, 5);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (24, 'b.intersection(a)', 0, 5);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (25, 'Стэк', 1, 6);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (26, 'Очередь', 0, 6);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (27, 'Дек', 1, 6);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (28, 'html', 1, 7);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (29, 'doc', 0, 7);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (30, 'cpp', 1, 7);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (31, 'pdf', 0, 7);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (32, 'xls', 0, 7);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (33, 'BufferIOBase', 1, 8);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (34, 'BufferWriter', 1, 8);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (35, 'BufferReader', 1, 8);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (36, 'StringReader', 0, 8);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (37, 'OutputStreamWriter', 0, 8);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (38, '''w'' нужен для записи в файл', 1, 9);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (39, '''w'' удаляет содержимое файла перед записью', 1, 9);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (40, '''w+'' не удалит содержимое файла', 0, 9);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (41, '''x'' несуществующий флаг', 0, 9);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (42, '''b'' открывает файл в бинарном режиме', 1, 9);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (43, 'run запускает поток', 0, 10);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (44, 'run вызывается при работе потока', 1, 10);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (45, 'в run описан функционал, работающий при запуске потока', 1, 10);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (46, 'run отвечает за запуск потока и его функционал', 0, 10);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (47, 'aсquire, закрывает Lock', 1, 11);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (48, 'close, закрывает Lock', 0, 11);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (49, 'acquit, открывает Lock', 0, 11);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (50, 'release, открывает Lock', 1, 11);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (51, 'aсquire, открывает Lock', 0, 11);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (52, 'getattr(y, locals()[x])()', 0, 12);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (53, 'getattr(locals()[x],y)(locals()[x])', 1, 12);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (54, 'locals()[x].y', 0, 12);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (55, 'x.y', 0, 12);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (56, 'globals(locals()[x],y)(locals()[x])', 1, 12);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (57, 'getattr(locals(x), y)(globals(x))', 0, 12);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (58, 'getattr(obj, attr, value) вернет атрибут attr у obj и присвоит ему значение value', 0, 13);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (59, 'hasattr(obj, attr) проверяет есть ли атрибут attr у obj, если да, то вернет его, если нет, то False', 0, 13);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (60, 'setattr(obj, attr, value) установит значение value у атрибута attr у obj', 1, 13);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (61, 'getattrs(obj) вернет все атрибуты у obj как словарь', 0, 13);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (62, 'getattr(obj, attr) вернет атрибут attr у obj', 1, 13);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (63, 'Применение средств языка к нему самому', 1, 14);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (64, 'Изучение атрибутов объектов во время выполнения программы', 0, 14);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (65, 'Техники анализа кода', 0, 14);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (66, 'Изменение реализации без изменения кода', 1, 14);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (67, 'Модификацию поведения программы во время выполнения программы', 1, 14);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (68, 'Выполняться нескольким потокам одновременно', 0, 15);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (69, 'Равномерно распределять нагрузку на потоки', 0, 15);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (70, 'Разрешать конфликты между потоками', 1, 15);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (71, 'Делать код потокобезопасным', 1, 15);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (72, 'Исключать ситуации, когда более одного потока нуждается в получении доступа к одной и той же переменной или ресурсу', 1, 15);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (73, 'f = open(filename, ''raf'')', 0, 16);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (74, 'f = open(filename, ''r'', random_access=True)', 0, 16);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (75, 'f = open(filename, ''r+b'')', 1, 16);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (76, 'with open(filename, ''r'') as random_access_file: ...', 0, 16);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (77, 'with open(filename, ''r+b'') as file: ...', 1, 16);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (78, 'tell', 1, 17);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (79, 'seek', 1, 17);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (80, 'get', 0, 17);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (81, 'move', 0, 17);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (82, 'set', 0, 17);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (83, 'создание экземпляра тестового класса', 1, 18);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (84, 'проверка на удобство использования', 0, 18);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (85, 'фикстуры', 1, 18);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (86, 'нагрузка для проверки производительности', 0, 18);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (87, 'Нулевой элемент входит в срез', 1, 19);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (88, 'Нулевой элемент не входит в срез', 0, 19);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (89, 'Длина среза зависит от длины самого списка', 0, 19);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (90, 'Длина среза не зависит от длины списка и её можно определить', 1, 19);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (91, 'str()', 1, 20);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (92, 'dict()', 0, 20);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (93, 'list()', 1, 20);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (94, 'set()', 0, 20);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (95, 'tuple()', 1, 20);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (96, 'Импортируемый файл с кодом', 1, 21);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (97, 'Часть кода которая комментируется', 0, 21);

INSERT INTO exam_testing_questionanswer (id, text, correct, question_id)
VALUES (98, 'Копия кода из других файлов в одном файле', 0, 21);
"""

with sqlite3.connect("db.sqlite3") as con:
    con.executescript(sql_script)
    sys.stdout.write("DB filled successfully")
