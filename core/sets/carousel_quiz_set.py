from typing import Dict

from .carousel_set import CarouselSet


class CarouselQuizSet(CarouselSet):
    def __init__(self, data):
        self.data = data

    def get_questions_and_answers(self) -> Dict[str, str]:
        return {entry["question"]: entry["perfectAnswer"] for entry in self.data}
