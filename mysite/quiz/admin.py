from django.contrib import admin
from django.contrib.admin import display

from .models import Question, Answer


class ChoiceInline(admin.TabularInline):
    model = Answer
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text', 'user']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'add_date', 'user')
    readonly_fields = ('user',)
    list_filter = ['add_date']
    search_fields = ['question_text']

    @display(ordering='book__author', description='User')
    def get_user(self, obj):
        return obj.user


admin.site.register(Question, QuestionAdmin)