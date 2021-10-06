from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.contrib import admin
import datetime


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    question_text = models.CharField(max_length=50)
    add_date = models.DateField('date added', default=timezone.now)

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE) # Deletes Answer if Question is deleted
    answer_text = models.CharField(max_length=200)

    def __str__(self):
        return self.answer_text


class DupeAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # Deletes Answer if Question is deleted
    answer_text = models.CharField(max_length=200)

    def __str__(self):
        return self.answer_text
