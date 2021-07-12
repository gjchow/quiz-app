from information import Information

OPTIONS = 3


class Quiz:
    def __init__(self, info: Information) -> None:
        self.info = info

    def begin(self) -> None:
        raise NotImplementedError


class Quiz_MC(Quiz):
    def begin(self) -> None:

        while True:  # TODO change this for an exit condition
            word = self.info.get_word()
            options = self.info.get_defs(OPTIONS, word)
            print(word)
            for num, option in enumerate(options):
                print(str(num + 1) + ': ' + option)
            choice = input()
            answer = options[int(choice)-1]
            correct = self.info.check_answer(word, answer)

            if correct:
                print('Correct!')

            else:
                print('Incorrect!')


class Quiz_Ans(Quiz):
    def begin(self) -> None:

        while True:
            word = self.info.get_word()
            defi = self.info.get_def(word)
            print(defi)
            answer = input()
            correct = self.info.check_answer(answer, defi)

            if correct:
                print('Correct!')

            else:
                print('Incorrect!')