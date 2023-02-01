# Testing website on Django
The purpose of the site is to get prepared for exam through passing all the questions
- if you answer on the question partly correct or incorrect, you will eventually have to answer it correctly (in next attempts)
- each new test is generated base on your previous answers (e.x. you will more likely see questions which you answered incorrectly than half-correct or even correct)
# How to run website
### 1. Make migrations
```shell
python manage.py makemigrations
```
### 2. Apply migrations
```shell
python manage.py migrate
```
### 3. Fill DB with questions (optional)
```shell
python fill_db.py
```
### 4. Run server
```shell
python manage.py runserver
```
***
### To add questions, you must have staff status, and then you should go to /admin
