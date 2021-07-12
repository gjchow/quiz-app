import random


class Information:
    def __init__(self) -> None:
        self.info = {}

    def get_info(self) -> None:
        # TODO fill out info
        # we can figure out using API or text file
        self.get_info_txt('test.txt')

    def get_info_txt(self, file: str):
        with open(file, 'r') as f:
            word = ""
            defs = []

            for data in f:
                data = data.strip()

                if len(data) != 0 and data[0] == '+':

                    if len(word) != 0 and len(defs) != 0:
                        self.info[word] = defs
                    word = data[1:]
                    defs = []

                elif len(data) != 0 and data[0] == '-':
                    defs.append(data[1:])

            if len(word) != 0 and len(defs) != 0:
                self.info[word] = defs

    def get_word(self) -> str:
        # return a random key from info
        word = random.choice(list(self.info.keys()))
        return word

    def get_def(self, word: str) -> str:
        # returns a random def of the word
        return random.choice(self.info[word])

    def get_defs(self, num: int, word: str) -> list[str]:
        # returns num options including at least one for the word
        defs = []

        defs.append(random.choice(self.info[word]))

        for _ in range(num - 1):
            pick = self.get_word()
            defs.append(random.choice(self.info[pick]))

        random.shuffle(defs)

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
