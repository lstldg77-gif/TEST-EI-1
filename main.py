"""한국사 퀴즈 게임 - 콘솔 프로그램 진입점"""

from default_quizzes import get_default_quizzes


class QuizGame:
    """퀴즈 게임 전체를 관리하는 클래스"""

    MENU = {
        1: "퀴즈 풀기",
        2: "퀴즈 추가",
        3: "퀴즈 목록",
        4: "점수 확인",
        5: "종료",
    }

    def __init__(self):
        self.running = True
        self.quizzes = get_default_quizzes()  # 퀴즈 목록 (list[Quiz])

    # ---------- 입력 처리 ----------
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

    # ---------- 메뉴 ----------
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

    def run(self):
        try:
            while self.running:
                self.show_menu()
                choice = self.read_number(f"메뉴를 선택하세요 (1-{len(self.MENU)}): ", 1, len(self.MENU))
                self.handle_choice(choice)
        except (KeyboardInterrupt, EOFError):
            print("\n\n[안내] 입력이 중단되어 프로그램을 안전하게 종료합니다.")

    def quit(self):
        print("\n게임을 종료합니다. 안녕히 가세요!")
        self.running = False

    # ---------- 기능 (구현 예정) ----------
    def play(self):
        """저장된 퀴즈를 순서대로 출제하고 결과를 보여준다."""
        if not self.quizzes:
            print("\n[안내] 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        total = len(self.quizzes)
        correct_count = 0
        print(f"\n퀴즈를 시작합니다! (총 {total}문제)")

        for number, quiz in enumerate(self.quizzes, start=1):
            quiz.display(number)
            user_answer = self.read_number("정답 번호를 입력하세요 (1-4): ", 1, 4)
            if quiz.is_correct(user_answer):
                print("  -> 정답입니다!")
                correct_count += 1
            else:
                print(f"  -> 오답입니다. 정답은 {quiz.answer}번 '{quiz.correct_choice()}'입니다.")

        score = self.calculate_score(correct_count, total)
        print("\n" + "-" * 40)
        print(f"결과: {total}문제 중 {correct_count}문제 정답 ({score}점)")
        print("-" * 40)
        return score

    def calculate_score(self, correct_count, total):
        """정답 수를 100점 만점 점수로 환산한다."""
        return round(correct_count / total * 100)

    def add_quiz(self):
        print("\n[안내] 퀴즈 추가 기능은 준비 중입니다.")

    def list_quizzes(self):
        print("\n[안내] 퀴즈 목록 기능은 준비 중입니다.")

    def show_score(self):
        print("\n[안내] 점수 확인 기능은 준비 중입니다.")


if __name__ == "__main__":
    QuizGame().run()
