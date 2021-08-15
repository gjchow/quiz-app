from django.db import models
from django.utils import timezone
from django.contrib import admin
import datetime


class Question(models.Model):
    question_text = models.CharField(max_length=50)
    add_date = models.DateField('date added', default=timezone.now)

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=200)

    def __str__(self):
        return self.answer_text
