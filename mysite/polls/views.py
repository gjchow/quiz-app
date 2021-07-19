from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from . import forms
from .information import Information
from .models import Question

#8CBED6


class IndexView(generic.TemplateView):
    template_name = 'polls/index.html'


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.ListView):
    model = Question
    paginate_by = 2
    template_name = 'polls/results.html'


def quiz_mc(request):
    info = Information()
    word = info.get_word()
    choices = info.get_defs(4, word)
    context = {'word': word, 'choices': choices}
    return render(request, 'polls/quiz-mc.html', context)


def quiz_text(request):
    info = Information()
    word = info.get_word()
    choices = info.get_defs(1, word)
    context = {'word': word, 'choices': choices}
    return render(request, 'polls/quiz-text.html', context)


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
            return HttpResponseRedirect(reverse('polls:quiz-mc'))

        if quiz == 'text':
            form = forms.TextForm(request.POST)
            if form.is_valid():
                val = form.cleaned_data["ans"]
                result = info.check_answer(val, str(given))
                print(val, given)
                print(result)
            return HttpResponseRedirect(reverse('polls:quiz-text'))


def add_new(request):
    info = Information()
    context = {}
    if request.method == 'POST':
        form = forms.FileForm(request.POST, request.FILES)
        if form.is_valid():
            num = info.handle_file(request.FILES['file'])
            context = {'num': num}
    print(context)
    return render(request, 'polls/add-new.html', context)