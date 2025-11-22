from PyQt5 import QtWidgets, QtCore
from extractor import extract_emails_only
from sound import play_click

class MisterAITool(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mister AI - Windows Tool")
        self.resize(1050, 650)

        self.setStyleSheet("""
            QWidget {
                background-color: #0c0c0c;
                color: #00eaff;
                font-family: Segoe UI;
                font-size: 14px;
            }
            QTextEdit, QLineEdit {
                background-color: #111;
                border: 1px solid #00eaff;
                border-radius: 4px;
                padding: 5px;
                color: #00eaff;
            }
            QGroupBox {
                border: 1px solid #00eaff;
                margin-top: 10px;
                padding: 10px;
            }
            QPushButton {
                padding: 12px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton#start { background-color: #00b300; color: #fff; }
            QPushButton#stop { background-color: #cc0000; color: #fff; }
            QPushButton#results { background-color: #333; color: #fff; }
            QPushButton#clear { background-color: #333; color: #fff; }
        """)

        layout = QtWidgets.QVBoxLayout(self)

        top = QtWidgets.QHBoxLayout()

        leftBox = QtWidgets.QGroupBox("KEYWORD LISTESI")
        leftLayout = QtWidgets.QVBoxLayout()
        self.keywordList = QtWidgets.QTextEdit()
        leftLayout.addWidget(self.keywordList)
        leftBox.setLayout(leftLayout)

        rightBox = QtWidgets.QGroupBox("COMBO FORMAT")
        rightLayout = QtWidgets.QVBoxLayout()
        self.fileBtn = QtWidgets.QPushButton("📁 اختر الملفات")
        self.fileBtn.clicked.connect(self.load_file)

        rightLayout.addWidget(self.fileBtn)
        rightBox.setLayout(rightLayout)

        top.addWidget(leftBox)
        top.addWidget(rightBox)

        btns = QtWidgets.QHBoxLayout()
        self.start = QtWidgets.QPushButton("ابدأ")
        self.start.setObjectName("start")

        self.stop = QtWidgets.QPushButton("إيقاف")
        self.stop.setObjectName("stop")

        self.clear = QtWidgets.QPushButton("تنظيف")
        self.clear.setObjectName("clear")
        self.clear.clicked.connect(self.clear_console)

        self.saveBtn = QtWidgets.QPushButton("💾 حفظ الإيميلات")
        self.saveBtn.setObjectName("results")
        self.saveBtn.clicked.connect(self.save_emails)

        for b in [self.start, self.stop, self.saveBtn, self.clear]:
            b.clicked.connect(play_click)
            btns.addWidget(b)

        self.console = QtWidgets.QTextEdit()
        self.console.setReadOnly(True)
        self.console.setFixedHeight(230)

        layout.addLayout(top)
        layout.addLayout(btns)
        layout.addWidget(self.console)

        # Transition effect
        effect = QtWidgets.QGraphicsOpacityEffect()
        self.setGraphicsEffect(effect)
        self.animation = QtCore.QPropertyAnimation(effect, b"opacity")
        self.animation.setDuration(900)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

    def load_file(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "اختر ملف", "", "Text Files (*.txt);;All Files (*)"
        )
        if not path:
            return

        self.console.append(f"📁 ملف مختار:\n{path}\n")
        emails = extract_emails_only(path)
        self.emails_list = emails

        count = len(emails)
        self.console.append(f"📊 عدد الإيميلات المستخرجة: {count}\n")

        if count > 0:
            for e in emails:
                self.console.append(e)
        else:
            self.console.append("❌ لا يوجد إيميلات في هذا الملف.")

    def save_emails(self):
        if not hasattr(self, "emails_list") or len(self.emails_list) == 0:
            self.console.append("⚠ لا يوجد إيميلات لحفظها.")
            return

        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "احفظ الملف", "emails.txt", "Text Files (*.txt)"
        )

        if path:
            with open(path, "w", encoding="utf-8") as f:
                for e in self.emails_list:
                    f.write(e + "\n")
            self.console.append(f"💾 تم حفظ {len(self.emails_list)} إيميل في:\n{path}")

    def clear_console(self):
        self.console.clear()
