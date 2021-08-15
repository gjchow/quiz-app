from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from . import forms
from .information import Information
from .models import Question

#8CBED6


class IndexView(generic.TemplateView):
    template_name = 'quiz/index.html'


class DetailView(generic.DetailView):
    model = Question
    template_name = 'quiz/detail.html'


class ResultsView(generic.ListView):
    model = Question
    paginate_by = 10
    template_name = 'quiz/results.html'


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
    context = {'page_obj': page_obj}

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
        context = {'word': word, 'choices': choices}
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
                print(given, val)
                print(result)
            return HttpResponseRedirect(reverse('quiz:quiz-mc'))

        if quiz == 'text':
            form = forms.TextForm(request.POST)
            if form.is_valid():
                val = form.cleaned_data["ans"]
                result = info.check_answer(val, str(given))
                print(val, given)
                print(result)
            return HttpResponseRedirect(reverse('quiz:quiz-text'))


def add_new(request):
    info = Information()
    context = {}
    if request.method == 'POST':
        form = forms.FileForm(request.POST, request.FILES)
        if form.is_valid():
            num, created = info.handle_file(request.FILES['file'])
            context = {'num': num, 'created': created}
    print(context)
    return render(request, 'quiz/add-new.html', context)