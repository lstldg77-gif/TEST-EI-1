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

    def to_dict(self):
        """JSON 저장을 위해 딕셔너리로 변환한다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    @classmethod
    def from_dict(cls, data):
        """딕셔너리로부터 Quiz 객체를 만든다. 형식이 잘못되면 ValueError를 발생시킨다."""
        if not isinstance(data, dict):
            raise ValueError("퀴즈 데이터가 딕셔너리 형식이 아닙니다.")
        question = data.get("question")
        choices = data.get("choices")
        answer = data.get("answer")
        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제(question)가 올바르지 않습니다.")
        if not isinstance(choices, list) or not all(isinstance(c, str) for c in choices):
            raise ValueError("선택지(choices)가 올바르지 않습니다.")
        if not isinstance(answer, int) or isinstance(answer, bool):
            raise ValueError("정답(answer)이 올바르지 않습니다.")
        return cls(question, choices, answer)
