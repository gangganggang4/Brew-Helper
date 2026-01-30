import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QComboBox, QLabel, QPushButton, 
                             QProgressBar, QTextBrowser, QFrame, QSplitter)
from PyQt6.QtCore import QTimer, Qt

class FinalBrewingHelper(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Planet Earth MC - 양조 마스터 헬퍼")
        self.setGeometry(100, 100, 1250, 800)

        self.brewing_db = {
            # 양조주
            "맥주": {"time": 11, "ing": "보리 4, 홉 2", "barrel": "모든 종류", "age": 2, "distill": "X", "price": "7.5", "alcohol": "13"},
            "크바스": {"time": 8, "ing": "빵 2, 설탕 3", "barrel": "가문비나무", "age": 2, "distill": "X", "price": "8.4", "alcohol": "16"},
            "밀맥주": {"time": 11, "ing": "밀 6, 홉 2", "barrel": "모든 종류", "age": 3, "distill": "X", "price": "9.8", "alcohol": "13"},
            "크릭 맥주": {"time": 12, "ing": "보리 6, 홉 2, 달콤한 열매 1", "barrel": "모든 종류", "age": 4, "distill": "X", "price": "11.8", "alcohol": "14"},
            "흑맥주": {"time": 13, "ing": "보리 5, 홉 2, 목탄 2", "barrel": "짙은 참나무", "age": 5, "distill": "X", "price": "11.7", "alcohol": "7"},
            "버터 맥주": {"time": 10, "ing": "보리 5, 홉 2, 버터 1, 계란 1", "barrel": "모든 종류", "age": 5, "distill": "X", "price": "14.4", "alcohol": "15"},
            "민들레주": {"time": 16, "ing": "민들레 8, 설탕 4", "barrel": "모든 종류", "age": 8, "distill": "X", "price": "18.9", "alcohol": "13"},
            "사과주": {"time": 12, "ing": "사과 4, 설탕 6", "barrel": "모든 종류", "age": 8, "distill": "X", "price": "36.0", "alcohol": "10"},
            "망고 사이다": {"time": 9, "ing": "망고 10, 설탕 3", "barrel": "정글 나무", "age": 7, "distill": "X", "price": "14.3", "alcohol": "7"},
            "빛나는 베리주": {"time": 8, "ing": "달콤한 열매 10, 발광 열매 1, 설탕 2", "barrel": "모든 종류", "age": 6, "distill": "X", "price": "11.0", "alcohol": "7"},
            "압생트": {"time": 16, "ing": "독감자 2, 잔디 6, 갈색 버섯 1", "barrel": "모든 종류", "age": 5, "distill": "X", "price": "12.2", "alcohol": "8"},
            "폴케": {"time": 14, "ing": "선인장 8, 설탕 4, 갈색 버섯 1", "barrel": "모든 종류", "age": 5, "distill": "X", "price": "12.2", "alcohol": "3"},
            "레드 와인": {"time": 15, "ing": "포도 12, 설탕 3", "barrel": "참나무", "age": 11, "distill": "X", "price": "15.3", "alcohol": "8"},
            "샴페인": {"time": 11, "ing": "포도 12, 설탕 3, 화약 1", "barrel": "참나무", "age": 10, "distill": "X", "price": "16.2", "alcohol": "10"},
            "사케": {"time": 14, "ing": "쌀 10, 갈색버섯 2", "barrel": "모든 종류", "age": 9, "distill": "X", "price": "13.9", "alcohol": "16"},
            "막걸리": {"time": 12, "ing": "쌀 8, 갈색 버섯 1, 설탕 1", "barrel": "모든 종류", "age": 4, "distill": "X", "price": "11.2", "alcohol": "8"},
            "염화주": {"time": 12, "ing": "네더와트 14, 석탄 4, 부싯돌 1", "barrel": "진홍빛 나무", "age": 66, "distill": "X", "price": "18", "alcohol": "20"},
            "한탄주": {"time": 15, "ing": "차가운 심장 2, 네더 와트 10", "barrel": "뒤틀린 나무", "age": 12, "distill": "X", "price": "52.0", "alcohol": "25"},
            "핫초코": {"time": 14, "ing": "코코아콩 32", "barrel": "X", "age": 0, "distill": "X", "price": "-", "alcohol": "-6"},
            
            # 증류주
            "위스키 (증류)": {"time": 10, "ing": "밀 8, 갈색 버섯 1", "barrel": "참나무", "age": 12, "distill": "3회", "price": "15.9", "alcohol": "40"},
            "버번 위스키 (증류)": {"time": 8, "ing": "옥수수 10, 밀 4", "barrel": "참나무", "age": 8, "distill": "5회", "price": "16.3", "alcohol": "50"},
            "피트 위스키 (증류)": {"time": 9, "ing": "밀 6, 옥수수 3, 갈색 버섯 1, 석탄 1", "barrel": "자작나무", "age": 10, "distill": "3회", "price": "17.5", "alcohol": "40"},
            "보드카 (증류)": {"time": 4, "ing": "감자 12, 갈색 버섯 1", "barrel": "X", "age": 0, "distill": "6회", "price": "9.3", "alcohol": "45"},
            "브랜디 (증류)": {"time": 12, "ing": "포도 12, 설탕 6", "barrel": "참나무", "age": 10, "distill": "3회", "price": "17.6", "alcohol": "40"},
        }

        self.remaining_time = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        splitter = QSplitter(Qt.Orientation.Horizontal)

        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        self.combo = QComboBox()
        self.combo.addItems(self.brewing_db.keys())
        self.combo.currentTextChanged.connect(self.display_recipe)
        
        self.recipe_display = QTextBrowser()
        
        left_layout.addWidget(QLabel("전체 술 레시피 리스트:"))
        left_layout.addWidget(self.combo)
        left_layout.addWidget(self.recipe_display)

        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_widget.setFixedWidth(400)

        timer_frame = QFrame()
        timer_frame.setFrameShape(QFrame.Shape.StyledPanel)
        timer_vbox = QVBoxLayout(timer_frame)

        self.status_label = QLabel("대기 중")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.timer_label = QLabel("00:00")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 60px; color: #2e7d32; font-weight: bold;")
        
        self.pbar = QProgressBar()
        
        btn_layout = QVBoxLayout()
        self.btn_ferment = QPushButton("발효 시작 (분 단위)")
        self.btn_age = QPushButton("숙성 시작 (20분=1년 단위)")
        self.btn_stop = QPushButton("정지")

        self.btn_ferment.clicked.connect(self.start_ferment_timer)
        self.btn_age.clicked.connect(self.start_aging_timer)
        self.btn_stop.clicked.connect(lambda: self.timer.stop())

        btn_layout.addWidget(self.btn_ferment)
        btn_layout.addWidget(self.btn_age)
        btn_layout.addWidget(self.btn_stop)

        timer_vbox.addWidget(self.status_label)
        timer_vbox.addWidget(self.timer_label)
        timer_vbox.addWidget(self.pbar)
        timer_vbox.addLayout(btn_layout)


        right_layout.addWidget(timer_frame)

        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        main_layout.addWidget(splitter)

        self.display_recipe(self.combo.currentText())

    def display_recipe(self, name):
        d = self.brewing_db[name]
        age_info = f"{d['age']}년 ({d['age']*20}분)" if d['age'] > 0 else "숙성 필요 없음"
        
        html = f"""
        <h2 style='color: #2e7d32;'>{name}</h2>
        <hr>
        <p style='font-size: 14px;'><b>재료:</b> {d['ing']}</p>
        <p style='font-size: 14px;'><b>발효 시간:</b> <span style='color: red;'>{d['time']}분</span></p>
        <p style='font-size: 14px;'><b>증류 횟수:</b> {d['distill']}</p>
        <p style='font-size: 14px;'><b>숙성:</b> {age_info}</p>
        <p style='font-size: 14px;'><b>배럴 종류:</b> {d['barrel']}</p>
        <hr>
        <p><b>가격:</b> {d['price']} G | <b>도수:</b> {d['alcohol']}%</p>
        """
        self.recipe_display.setHtml(html)

    def start_ferment_timer(self):
        name = self.combo.currentText()
        mins = self.brewing_db[name]['time']
        self.setup_timer(mins, f"[{name}] 발효 중...")

    def start_aging_timer(self):
        name = self.combo.currentText()
        years = self.brewing_db[name]['age']
        if years == 0: return
        self.setup_timer(years * 20, f"[{name}] 숙성 중 ({years}년)...")

    def setup_timer(self, total_mins, status_text):
        self.remaining_time = total_mins * 60
        self.pbar.setMaximum(self.remaining_time)
        self.pbar.setValue(self.remaining_time)
        self.status_label.setText(status_text)
        self.timer.start(1000)

    def update_timer(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            mins, secs = divmod(self.remaining_time, 60)
            self.timer_label.setText(f"{mins:02d}:{secs:02d}")
            self.pbar.setValue(self.remaining_time)
        else:
            self.timer.stop()
            self.timer_label.setText("알람!!")
            self.status_label.setText("공정 완료! 확인하세요.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FinalBrewingHelper()
    window.show()
    sys.exit(app.exec())
