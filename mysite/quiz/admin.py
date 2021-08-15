from django.contrib import admin
from .models import Question, Answer


class ChoiceInline(admin.TabularInline):
    model = Answer
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'add_date')
    list_filter = ['add_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)