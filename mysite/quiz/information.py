import random

from django.conf import settings
from django.contrib.auth.models import User

from .models import Question, Answer, DupeAnswer


class Information:
    # def get_info(self):
    #     # fill out info
    #     # we can figure out using API or text file
    #     self.get_info_txt('test.txt')
    def __init__(self, user: User):
        self.user = user

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

    def _get_word(self, excl='') -> Question:
        # return a random key from info
        num = self.user.question_set.all().exclude(question_text=excl).count()
        if num > 0:
            word = self.user.question_set.all().exclude(question_text=excl)[random.randrange(num)]
        else:
            word = None

        return word

    def _get_word_def(self, q: Question) -> list[Answer]:
        defs = []
        c = q.answer_set.count()

        defs.append(q.answer_set.all()[random.randrange(c)])

        return defs

    def _get_defs(self, num: int, q: Question) -> list[Answer]:
        # returns num options including at least one for the word
        defs = []

        for _ in range(num):
            pick = self._get_word(q.question_text)
            c = pick.answer_set.count()
            defs.append(pick.answer_set.all()[random.randrange(c)])

        random.shuffle(defs)

        return defs

    def get_question(self, num: int) -> tuple[Question, list[Answer]]:
        word = None
        choices = []
        if num > self.user.question_set.all().count():
            return word, choices
        dupe_set = DupeAnswer.objects.all().filter(question__user=self.user)
        if DupeAnswer.objects.all().filter(question__user=self.user).exists():
            roll = random.randrange(10)
            # if settings.DEBUG:
            #     print('Exists')
            #     print(roll)
            if roll < 2:
                dupe_set = DupeAnswer.objects.all().filter(question__user=self.user)
                c = dupe_set.count()
                da = dupe_set[random.randrange(c)]
                word = da.question
                choices.append(da)
                choices.extend(self._get_defs(num-1, word))
            else:
                word = self._get_word()
                choices = self._get_word_def(word)
                choices.extend(self._get_defs(num-1, word))
        else:
            # if settings.DEBUG:
            #     print('DNE')
            word = self._get_word()
            choices = self._get_word_def(word)
            choices.extend(self._get_defs(num - 1, word))
        random.shuffle(choices)
        return word, choices

    def check_answer(self, word: str, answer: str) -> bool:
        # if settings.DEBUG:
        #     print('Check: ', DupeAnswer.objects.all())
        qs = self.user.question_set.all().filter(question_text=word)
        if not qs:
            return False

        for q in qs:
            if q.answer_set.all().filter(answer_text=answer):
                return True

        return False

    def get_ans_index(self, word: Question,  answers: list[Answer]):
        for i in range(len(answers)):
            if self.check_answer(str(word), str(answers[i])):
                return i
        return -1

    def add_data(self, info: dict[str: list[str]]) -> tuple[int, int, str]:
        added = 0
        edited = 0
        add_word = None
        for word in info:
            if self.user.question_set.all().filter(question_text=word).exists():
                new = self.user.question_set.all().filter(question_text=word)[0]
                added += 1
            else:
                new = Question(question_text=word, user=self.user)
                new.save()
                edited += 1
            for defs in info[word]:
                if not new.answer_set.all().filter(answer_text=defs).exists():
                    new.answer_set.create(answer_text=defs)
            if added + edited == 1:
                add_word = word
        return added, edited, add_word

    def handle_file(self, f) -> tuple[int, int, str]:
        info = self.get_info_txt(f)
        added, edited, add_word = self.add_data(info)
        return added, edited, add_word

    def update_word(self, word: str, defs: list[str]) -> None:
        if self.user.question_set.all().filter(question_text=word).exists():
            quest = self.user.question_set.all().filter(question_text=word)[0]
            quest.answer_set.all().delete()
            for defi in defs:
                if not quest.answer_set.all().filter(answer_text=defi).exists():
                    quest.answer_set.create(answer_text=defi)

    def delete_word(self, pk: int) -> None:
        if self.user.question_set.all().filter(pk=pk).exists():
            self.user.question_set.all().filter(pk=pk).delete()

    def dupe_answer(self, word, defi):
        question = self.user.question_set.all().filter(question_text=word)[0]
        question.dupeanswer_set.create(answer_text=defi)

    def delete_dupe(self, word, defi):
        question = self.user.question_set.all().filter(question_text=word)[0]
        if question.dupeanswer_set.filter(answer_text=defi).exists():
            question.dupeanswer_set.filter(answer_text=defi)[0].delete()

    def reset_dupe(self):
        dupe_set = DupeAnswer.objects.all().filter(question__user=self.user)
        print(dupe_set)
        print(DupeAnswer.objects.all())