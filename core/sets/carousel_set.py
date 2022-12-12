from abc import ABC
from typing import Dict


class CarouselSet(ABC):
    def get_questions_and_answers(self) -> Dict[str, str]:
        pass
