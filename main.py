from information import Information
from quiz import Quiz_MC

if __name__ == "__main__":
    information = Information()
    information.get_info()
    print(information.info)
    quiz = Quiz_MC(information)

    quiz.begin()
