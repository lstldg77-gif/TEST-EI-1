"""개별 퀴즈를 표현하는 Quiz 클래스"""


class Quiz:
    """문제 하나(문제, 선택지 4개, 정답 번호)를 표현하는 클래스"""

    CHOICE_COUNT = 4

    def __init__(self, question, choices, answer):
        if len(choices) != Quiz.CHOICE_COUNT:
            raise ValueError(f"선택지는 {Quiz.CHOICE_COUNT}개여야 합니다.")
        if not 1 <= answer <= Quiz.CHOICE_COUNT:
            raise ValueError(f"정답은 1~{Quiz.CHOICE_COUNT} 사이의 번호여야 합니다.")
        self.question = question   # 문제 (str)
        self.choices = list(choices)  # 선택지 (list[str], 4개)
        self.answer = answer       # 정답 번호 (int, 1~4)

    def display(self, number=None):
        """문제와 선택지를 화면에 출력한다."""
        title = f"[문제 {number}] " if number is not None else ""
        print(f"\n{title}{self.question}")
        for index, choice in enumerate(self.choices, start=1):
            print(f"  {index}. {choice}")

    def is_correct(self, user_answer):
        """사용자가 고른 번호가 정답이면 True를 반환한다."""
        return user_answer == self.answer

    def correct_choice(self):
        """정답 선택지의 내용을 반환한다."""
        return self.choices[self.answer - 1]
