import random

from django.utils import timezone
from django.db.models import Max

from .models import Question, Answer


class Information:
    # def get_info(self):
    #     # fill out info
    #     # we can figure out using API or text file
    #     self.get_info_txt('test.txt')

    def get_info_txt(self, file):
        info = {}
        word = ""
        defs = []

        for line in file:
            line = line.decode(encoding='UTF-8', errors='strict')
            line = line.strip()

            if len(line) != 0 and line[0] == '+':

                if len(word) != 0 and len(defs) != 0:
                    if word in info:
                        info[word].extend(defs)
                    else:
                        info[word] = defs
                word = line[1:]
                defs = []

            elif len(line) > 1 and line[0] == '-':
                defs.append(line[1:])

        if len(word) != 0 and len(defs) != 0:
            if word in info:
                info[word].extend(defs)
            else:
                info[word] = defs
        return info

    def get_word(self, excl='') -> Question:
        # return a random key from info
        num = Question.objects.exclude(question_text=excl).count()
        if num > 0:
            word = Question.objects.exclude(question_text=excl)[random.randrange(num)]
        else:
            word = None

        return word

    def get_defs(self, num: int, q: Question) -> list[Answer]:
        # returns num options including at least one for the word
        defs = []
        c = q.answer_set.count()

        defs.append(q.answer_set.all()[random.randrange(c)])

        for _ in range(num - 1):
            pick = self.get_word(q.question_text)
            c = pick.answer_set.count()
            defs.append(pick.answer_set.all()[random.randrange(c)])

        random.shuffle(defs)

        return defs

    def check_answer(self, word: str, answer: str) -> bool:
        qs = Question.objects.filter(question_text=word)
        if not qs:
            return False

        for q in qs:
            if q.answer_set.all().filter(answer_text=answer):
                return True

        return False

    def get_ans_index(self, word: str,  answers: list[Answer]):
        for i in range(len(answers)):
            if self.check_answer(word, str(answers[i])):
                return i
        return -1

    def add_data(self, info):
        added = 0
        edited = 0
        add_word = None
        for word in info:
            if Question.objects.filter(question_text=word).exists():
                new = Question.objects.filter(question_text=word)[0]
                added += 1
            else:
                new = Question(question_text=word)
                new.save()
                edited += 1
            for defs in info[word]:
                if not new.answer_set.all().filter(answer_text=defs).exists():
                    new.answer_set.create(answer_text=defs)
            if added + edited == 1:
                add_word = word
        return added, edited, add_word

    def handle_file(self, f):
        info = self.get_info_txt(f)
        added, edited, add_word = self.add_data(info)
        return added, edited, add_word

    def update_word(self, word, defs):
        if Question.objects.filter(question_text=word).exists():
            quest = Question.objects.filter(question_text=word)[0]
            quest.answer_set.all().delete()
            for defi in defs:
                if not quest.answer_set.all().filter(answer_text=defi).exists():
                    quest.answer_set.create(answer_text=defi)

