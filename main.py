from pyperclip import copy

from core.carousel import Carousel


def main():
    forename = input("Forename?\n > ").strip()
    surname = input("Surname?\n > ").strip()

    carousel = Carousel(forename, surname)

    set_id = input("Id of set?\n > ")
    is_quiz = input("Is quiz? y/n\n > ").lower().lstrip() == "y"

    if is_quiz:
        carousel_set = carousel.get_quiz_set(set_id)

    else:
        carousel_set = carousel.get_study_pack_set(set_id)

    quiz_qa = carousel_set.get_questions_and_answers()

    paste_text = Carousel.convert_question_and_answers_to_study_smarter(quiz_qa)
    copy(paste_text)

    print("Copied to clipboard")


if __name__ == "__main__":
    main()
