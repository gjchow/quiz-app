from information import Information

OPTIONS = 3


class Quiz:
    def __init__(self, info: Information) -> None:
        self.info = info

    def begin(self):
        while True:  # TODO change this for an exit condition
            word = self.info.get_word()
            options = self.info.get_defs(OPTIONS, word)
            print(word)
            for num, option in enumerate(options):
                print(str(num) + ': ' + option)
