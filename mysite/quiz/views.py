from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.forms import formset_factory, model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy

from . import forms
from .information import Information
from .models import Question

THEME = 'light'


def index(request):
    template_name = 'quiz/index.html'
    context = {'theme': THEME}
    current_user = request.user
    if current_user.is_authenticated:
        info = Information(request.user)
        info.reset_dupe()
    return render(request, template_name, context)


@login_required
def detail(request, pk):
    info = Information(request.user)
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
    context = {'question': question, 'formseta': formseta, 'theme': THEME}
    return render(request, 'quiz/detail.html', context)


@login_required
def delete(request, pk):
    info = Information(request.user)
    info.delete_word(pk)
    return HttpResponseRedirect(reverse('quiz:list'))


@login_required
def listing(request):
    if request.method == 'POST':
        form = forms.SearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data["search"]
            return HttpResponseRedirect(reverse('quiz:search', args=(search,)))
        else:
            question_list = Question.objects.all().order_by('question_text')
    else:
        question_list = request.user.question_set.all().order_by('question_text')
    paginator = Paginator(question_list, 10)
    template_name = 'quiz/results.html'
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'theme': THEME}

    return render(request, template_name, context)


@login_required
def search_list(request, search):
    question_list = request.user.question_set.filter(question_text__contains=search).order_by('question_text')
    paginator = Paginator(question_list, 10)
    template_name = 'quiz/results.html'
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'search': search, 'theme': THEME}

    return render(request, template_name, context)


@login_required
def quiz_mc(request):
    info = Information(request.user)
    word, choices = info.get_question(4)
    # if settings.DEBUG:
    #     print(word, choices)
    ans_ind = info.get_ans_index(word, choices)
    context = {'word': word, 'choices': choices, 'ans_ind': ans_ind, 'theme': THEME}
    return render(request, 'quiz/quiz-mc.html', context)


@login_required
def quiz_text(request):
    info = Information(request.user)
    word, choices = info.get_question(1)
    # if settings.DEBUG:
    #     print(word, choices)
    context = {'word': str(word), 'choices': choices, 'theme': THEME}
    return render(request, 'quiz/quiz-text.html', context)


@login_required
def check_ans(request, quiz, given):
    info = Information(request.user)
    if request.method == 'POST':
        if quiz == 'mc':
            form = forms.MCForm(request.POST)
            if form.is_valid():
                val = form.cleaned_data["choice"]
                correct = form.cleaned_data["correct"]
                result = info.check_answer(given, val)
                if not result:
                    info.dupe_answer(given, correct)
                else:
                    info.delete_dupe(given, correct)
                # if settings.DEBUG:
                #     print(result)
                #     print(given, val)
            return HttpResponseRedirect(reverse('quiz:quiz-mc'))

        if quiz == 'text':
            form = forms.TextForm(request.POST)
            if form.is_valid():
                val = form.cleaned_data["ans"]
                correct = form.cleaned_data["correct"]
                result = info.check_answer(val, given)
                if not result:
                    info.dupe_answer(correct, given)
                else:
                    info.delete_dupe(correct, given)
                # if settings.DEBUG:
                #     print(result)
                #     print(val, given)
            return HttpResponseRedirect(reverse('quiz:quiz-text'))


@login_required
def add_new(request):
    info = Information(request.user)
    AnswerFormSet = formset_factory(forms.AnswerForm, extra=0, max_num=10, min_num=1, validate_min=True)
    nformq = forms.QuestionForm()
    nformseta = AnswerFormSet()
    context = {'formseta': nformseta, 'formq': nformq, 'theme': THEME}
    if request.method == 'POST':
        formq = forms.QuestionForm(request.POST)
        formseta = AnswerFormSet(request.POST)
        formfile = forms.FileForm(request.POST, request.FILES)
        if formfile.is_valid():
            num, created, add_word = info.handle_file(request.FILES['file'])
            context = {'num': num, 'created': created, 'formseta': nformseta, 'formq': nformq, 'theme': THEME}
        if formq.is_valid() and formseta.is_valid():
            answers = []
            question = formq.cleaned_data['question_text']
            for forma in formseta:
                if 'answer_text' in forma.cleaned_data:
                    answer = forma.cleaned_data['answer_text']
                    answers.append(answer)
            data = {question: answers}
            num, created, add_word = info.add_data(data)
            context = {'add_word': add_word, 'formseta': nformseta, 'formq': nformq, 'theme': THEME}
    return render(request, 'quiz/add-new.html', context)


def signup(request):
    template_name = 'registration/signup.html'
    if request.method == 'POST':
        form = forms.UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(username, password=password)
        return HttpResponseRedirect(reverse_lazy('login'))
    return render(request, template_name)
