from information import Information
from quiz import Quiz

if __name__ == "__main__":
    information = Information()
    information.get_info()
    quiz = Quiz(information)

    quiz.begin()
