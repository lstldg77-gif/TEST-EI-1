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
        print("\n[안내] 퀴즈 풀기 기능은 준비 중입니다.")

    def add_quiz(self):
        print("\n[안내] 퀴즈 추가 기능은 준비 중입니다.")

    def list_quizzes(self):
        print("\n[안내] 퀴즈 목록 기능은 준비 중입니다.")

    def show_score(self):
        print("\n[안내] 점수 확인 기능은 준비 중입니다.")


if __name__ == "__main__":
    QuizGame().run()
