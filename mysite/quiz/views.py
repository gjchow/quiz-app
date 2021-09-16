from django.core.paginator import Paginator
from django.forms import formset_factory, model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from . import forms
from .information import Information
from .models import Question


class IndexView(generic.TemplateView):
    template_name = 'quiz/index.html'


def detail(request, pk):
    info = Information()
    AnswerFormSet = formset_factory(forms.AnswerForm, extra=0, max_num=10, min_num=1, validate_min=True)
    question = Question.objects.get(pk=pk)
    if request.method == 'POST':
        formseta = AnswerFormSet(request.POST)
        if formseta.is_valid():
            answers = []
            for forma in formseta:
                if 'answer_text' in forma.cleaned_data:
                    answer = forma.cleaned_data['answer_text']
                    answers.append(answer)
            info.update_word(question, answers)
    answers = []
    for ans in question.answer_set.all():
        answers.append(model_to_dict(ans, fields='answer_text'))
    formseta = AnswerFormSet(initial=answers)
    context = {'question': question, 'formseta': formseta}
    return render(request, 'quiz/detail.html', context)


def delete(request, pk):
    info = Information()
    info.delete_word(pk)
    return HttpResponseRedirect(reverse('quiz:list'))


def listing(request):
    if request.method == 'POST':
        form = forms.SearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data["search"]
            return HttpResponseRedirect(reverse('quiz:search', args=(search,)))
        else:
            question_list = Question.objects.all().order_by('question_text')
    else:
        question_list = Question.objects.all().order_by('question_text')
    paginator = Paginator(question_list, 10)
    template_name = 'quiz/results.html'
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}

    return render(request, template_name, context)


def search_list(request, search):
    question_list = Question.objects.filter(question_text__contains=search).order_by('question_text')
    paginator = Paginator(question_list, 10)
    template_name = 'quiz/results.html'
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'search': search}

    return render(request, template_name, context)


def quiz_mc(request):
    info = Information()
    word = info.get_word()
    if word is not None:
        choices = info.get_defs(4, word)
        ans_ind = info.get_ans_index(word, choices)
        context = {'word': word, 'choices': choices, 'ans_ind': ans_ind}
    else:
        context = {'word': word}
    return render(request, 'quiz/quiz-mc.html', context)


def quiz_text(request):
    info = Information()
    word = info.get_word()
    if word is not None:
        choices = info.get_defs(1, word)
        context = {'word': str(word), 'choices': choices}
    else:
        context = {'word': word}
    return render(request, 'quiz/quiz-text.html', context)


def check_ans(request, quiz, given):
    info = Information()
    if request.method == 'POST':

        if quiz == 'mc':
            form = forms.MCForm(request.POST)
            if form.is_valid():
                val = form.cleaned_data["choice"]
                result = info.check_answer(str(given), val)
            return HttpResponseRedirect(reverse('quiz:quiz-mc'))

        if quiz == 'text':
            form = forms.TextForm(request.POST)
            if form.is_valid():
                val = form.cleaned_data["ans"]
                result = info.check_answer(val, str(given))
            return HttpResponseRedirect(reverse('quiz:quiz-text'))


def add_new(request):
    info = Information()
    AnswerFormSet = formset_factory(forms.AnswerForm, extra=0, max_num=10, min_num=1, validate_min=True)
    nformq = forms.QuestionForm()
    nformseta = AnswerFormSet()
    context = {'formseta': nformseta, 'formq': nformq}
    if request.method == 'POST':
        formq = forms.QuestionForm(request.POST)
        formseta = AnswerFormSet(request.POST)
        formfile = forms.FileForm(request.POST, request.FILES)
        if formfile.is_valid():
            num, created, add_word = info.handle_file(request.FILES['file'])
            context = {'num': num, 'created': created, 'formseta': nformseta, 'formq': nformq}
        if formq.is_valid() and formseta.is_valid():
            answers = []
            question = formq.cleaned_data['question_text']
            for forma in formseta:
                if 'answer_text' in forma.cleaned_data:
                    answer = forma.cleaned_data['answer_text']
                    answers.append(answer)
            data = {question: answers}
            num, created, add_word = info.add_data(data)
            context = {'add_word': add_word, 'formseta': nformseta, 'formq': nformq}
    return render(request, 'quiz/add-new.html', context)
