"""게임 전체(메뉴, 게임 진행, 데이터 저장)를 관리하는 QuizGame 클래스"""

import json
import os

from default_quizzes import get_default_quizzes
from quiz import Quiz

# 프로젝트 루트(이 파일이 있는 폴더)의 state.json
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")


class QuizGame:
    """퀴즈 목록과 최고 점수를 보관하고, 메뉴에 따라 기능을 실행하는 클래스"""

    MENU = {
        1: "퀴즈 풀기",
        2: "퀴즈 추가",
        3: "퀴즈 목록",
        4: "점수 확인",
        5: "종료",
    }

    def __init__(self, state_file=STATE_FILE):
        self.state_file = state_file  # 데이터 파일 경로 (str)
        self.quizzes = []             # 퀴즈 목록 (list[Quiz])
        self.best_score = None        # 최고 점수 (int 0~100, 아직 풀지 않았으면 None)
        self.running = True           # 메뉴 반복 여부 (bool)
        self.load()

    # ================= 실행 / 메뉴 =================
    def run(self):
        """메뉴를 반복해서 보여주고 선택한 기능을 실행한다."""
        try:
            while self.running:
                self.show_menu()
                choice = self.read_number(
                    f"메뉴를 선택하세요 (1-{len(self.MENU)}): ", 1, len(self.MENU)
                )
                self.handle_choice(choice)
        except (KeyboardInterrupt, EOFError):
            print("\n\n[안내] 입력이 중단되었습니다. 데이터를 저장하고 안전하게 종료합니다.")
            self.save()

    def show_menu(self):
        print("\n" + "=" * 40)
        print("          한국사 퀴즈 게임")
        print("=" * 40)
        for number, title in self.MENU.items():
            print(f"  {number}. {title}")
        print("=" * 40)

    def handle_choice(self, choice):
        if choice == 1:
            self.play()
        elif choice == 2:
            self.add_quiz()
        elif choice == 3:
            self.list_quizzes()
        elif choice == 4:
            self.show_score()
        else:
            self.quit()

    def quit(self):
        self.save()
        print("\n데이터를 저장했습니다. 게임을 종료합니다. 안녕히 가세요!")
        self.running = False

    # ================= 입력 처리 =================
    def read_number(self, prompt, min_value, max_value):
        """min_value~max_value 범위의 정수를 입력받을 때까지 반복한다."""
        while True:
            text = input(prompt).strip()
            if not text:
                print("[안내] 입력이 비어 있습니다. 숫자를 입력해 주세요.")
                continue
            try:
                number = int(text)
            except ValueError:
                print(f"[안내] '{text}'은(는) 숫자가 아닙니다. 숫자를 입력해 주세요.")
                continue
            if not min_value <= number <= max_value:
                print(f"[안내] {min_value}~{max_value} 사이의 숫자를 입력해 주세요.")
                continue
            return number

    def read_text(self, prompt):
        """비어 있지 않은 문자열을 입력받을 때까지 반복한다."""
        while True:
            text = input(prompt).strip()
            if text:
                return text
            print("[안내] 입력이 비어 있습니다. 내용을 입력해 주세요.")

    # ================= 게임 진행 =================
    def play(self):
        """저장된 퀴즈를 순서대로 출제하고 결과와 최고 점수를 보여준다."""
        if not self.quizzes:
            print("\n[안내] 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return None

        total = len(self.quizzes)
        correct_count = 0
        print(f"\n퀴즈를 시작합니다! (총 {total}문제)")

        for number, quiz in enumerate(self.quizzes, start=1):
            quiz.display(number)
            user_answer = self.read_number(
                f"정답 번호를 입력하세요 (1-{Quiz.CHOICE_COUNT}): ", 1, Quiz.CHOICE_COUNT
            )
            if quiz.is_correct(user_answer):
                print("  -> 정답입니다!")
                correct_count += 1
            else:
                print(f"  -> 오답입니다. 정답은 {quiz.answer}번 '{quiz.correct_choice()}'입니다.")

        score = self.calculate_score(correct_count, total)
        print("\n" + "-" * 40)
        print(f"결과: {total}문제 중 {correct_count}문제 정답 ({score}점)")
        print("-" * 40)

        if self.update_best_score(score):
            print(f"[축하] 최고 점수를 갱신했습니다! ({score}점)")
        else:
            print(f"현재 최고 점수: {self.best_score}점")
        self.save()
        return score

    def calculate_score(self, correct_count, total):
        """정답 수를 100점 만점 점수로 환산한다."""
        return round(correct_count / total * 100)

    def update_best_score(self, score):
        """새 점수가 최고 점수보다 높으면 갱신하고 True를 반환한다."""
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            return True
        return False

    def add_quiz(self):
        """문제, 선택지 4개, 정답 번호를 입력받아 퀴즈를 등록하고 저장한다."""
        print("\n새 퀴즈를 등록합니다.")
        question = self.read_text("문제를 입력하세요: ")
        choices = []
        for index in range(1, Quiz.CHOICE_COUNT + 1):
            choices.append(self.read_text(f"선택지 {index}: "))
        answer = self.read_number(
            f"정답 번호를 입력하세요 (1-{Quiz.CHOICE_COUNT}): ", 1, Quiz.CHOICE_COUNT
        )

        self.quizzes.append(Quiz(question, choices, answer))
        if self.save():
            print(f"[완료] 퀴즈가 추가되었습니다. (현재 {len(self.quizzes)}문제)")

    def list_quizzes(self):
        """등록된 퀴즈 목록(문제와 선택지)을 출력한다. 정답은 공개하지 않는다."""
        if not self.quizzes:
            print("\n[안내] 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return
        print(f"\n등록된 퀴즈 목록 (총 {len(self.quizzes)}문제)")
        for number, quiz in enumerate(self.quizzes, start=1):
            quiz.display(number)

    def show_score(self):
        """저장된 최고 점수를 출력한다."""
        if self.best_score is None:
            print("\n[안내] 아직 퀴즈를 풀지 않았습니다. 퀴즈를 풀면 최고 점수가 기록됩니다.")
            return
        print(f"\n최고 점수: {self.best_score}점 (100점 만점)")

    # ================= 파일 저장 / 불러오기 =================
    def load(self):
        """state.json에서 퀴즈와 최고 점수를 불러온다."""
        if not os.path.exists(self.state_file):
            # 첫 실행: 기본 퀴즈 데이터 사용
            self.reset_to_default()
            return
        try:
            with open(self.state_file, "r", encoding="utf-8") as file:
                data = json.load(file)
            quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]
            best_score = data.get("best_score")
            if best_score is not None and (
                not isinstance(best_score, int) or isinstance(best_score, bool)
                or not 0 <= best_score <= 100
            ):
                raise ValueError("best_score 값이 올바르지 않습니다.")
        except (OSError, ValueError, KeyError, TypeError) as error:
            # json.JSONDecodeError, UnicodeDecodeError 는 ValueError의 하위 클래스
            print(f"[안내] 데이터 파일(state.json)을 읽을 수 없습니다: {error}")
            print("[안내] 기본 퀴즈 데이터로 복구합니다.")
            self.reset_to_default()
            self.save()
            return
        self.quizzes = quizzes
        self.best_score = best_score

    def save(self):
        """현재 퀴즈와 최고 점수를 state.json에 UTF-8로 저장한다. 성공하면 True."""
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
        }
        try:
            with open(self.state_file, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
            return True
        except OSError as error:
            print(f"[안내] 데이터를 저장하지 못했습니다: {error}")
            return False

    def reset_to_default(self):
        """기본 퀴즈 데이터로 초기화한다."""
        self.quizzes = get_default_quizzes()
        self.best_score = None
