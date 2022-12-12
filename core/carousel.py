from typing import Dict

import requests as requests

from .sets.carousel_quiz_set import CarouselQuizSet
from .sets.carousel_set import CarouselSet
from .sets.carousel_study_pack_set import CarouselStudyPackSet

ROW_SEPARATOR = "\n\\#\n"
TERM_SEPARATOR = "/#*#/"

LOGIN_URL = "https://api.carousel-learning.com/api/auth/student/token"

QUIZ_BASE_URL = "https://api.carousel-learning.com/api/open/quizzes/"
QUIZ_QUESTIONS_URL = lambda \
    quiz_id: f"https://api.carousel-learning.com/api/student/quizzes/{quiz_id}/questions/revision"

STUDY_PACK_BASE_URL = "https://api.carousel-learning.com/api/open/independent-learning/study-pack/"
STUDY_PACK_QUESTIONS_URL = lambda \
        study_pack_id: f"https://api.carousel-learning.com/api/student/independent-learning/quiz-sets/study-pack/{study_pack_id}"


class Carousel:
    def __init__(self, forename: str, surname: str):
        self.forename = forename
        self.surname = surname

        self._session = requests.Session()

        self._session.headers["referer"] = "https://app.carousel-learning.com/"
        self._session.headers["accept"] = "application/json, text/plain, */*"
        self._session.headers["origin"] = "https://app.carousel-learning.com"

    def _login(self, teaching_group_id: str) -> str:
        res = self._session.post(LOGIN_URL, {
            "forename": self.forename,
            "surname": self.surname,
            "teachingGroupId": teaching_group_id
        })

        return "Bearer " + res.json()["token"]

    def get_quiz_set(self, quiz_id: str) -> CarouselSet:
        info = self._session.get(QUIZ_BASE_URL + quiz_id)
        teaching_group_id = info.json()["data"]["teachingGroup"]["data"]["id"]

        auth_token = self._login(teaching_group_id)

        raw_res = self._session.get(QUIZ_QUESTIONS_URL(quiz_id),
                                    headers={"authorization": auth_token})
        question_data = raw_res.json()["data"]

        return CarouselQuizSet(question_data)

    def get_study_pack_set(self, study_pack_id: str) -> CarouselSet:
        info = self._session.get(STUDY_PACK_BASE_URL + study_pack_id)
        teaching_group_id = info.json()["data"]["teachingGroup"]["data"]["id"]

        auth_token = self._login(teaching_group_id)

        raw_res = self._session.get(STUDY_PACK_QUESTIONS_URL(study_pack_id),
                                    headers={"authorization": auth_token})
        question_data = raw_res.json()["data"]["studyPack"]["data"]["questions"]["data"]

        return CarouselStudyPackSet(question_data)

    @staticmethod
    def convert_question_and_answers_to_study_smarter(questions_and_answers: Dict[str, str]) -> str:
        return ROW_SEPARATOR.join([f"{k}{TERM_SEPARATOR}{v}" for k, v in questions_and_answers.items()])

