import random


class Information:
    def __init__(self) -> None:
        self.info = {}

    def get_info(self) -> None:
        # TODO fill out info
        # we can figure out using API or text file
        self.info['a'] = ['a']
        self.info['b'] = ['b']
        self.info['c'] = ['c']
        self.info['d'] = ['d']
        self.info['e'] = ['e']


    def get_word(self) -> str:
        # return a random key from info
        word = random.choice(list(self.info.keys()))
        return word

    def get_defs(self, num: int, word: str) -> list[str]:
        # returns num options including at least one for the word
        defs = []

        defs.append(random.choice(self.info[word]))
        for _ in range(num - 1):
            pick = self.get_word()
            defs.append(random.choice(self.info[pick]))

        return defs

    def check_answer(self, word: str, answer: str) -> bool:
        # check if the word exists in info
        if word not in self.info:
            return False

        # check if answer is a value for word in info
        if answer not in self.info[word]:
            return False
        else:
            return True
