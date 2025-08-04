import sys
import math
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QCheckBox, QLabel, QTabWidget, QTextEdit, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class CalcForge(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CalcForge")
        self.setGeometry(200, 200, 600, 700)

        self.history = []
        self.current_expression = ""
        self.dark_mode = True

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Theme Toggle
        self.theme_toggle = QCheckBox("🌓Theme")
        self.theme_toggle.setChecked(True)
        self.theme_toggle.stateChanged.connect(self.toggle_theme)
        main_layout.addWidget(self.theme_toggle)

        # Tabs: Calculator and History
        self.tabs = QTabWidget()
        self.calc_tab = QWidget()
        self.history_tab = QWidget()

        self.tabs.addTab(self.calc_tab, "Calculator")
        self.tabs.addTab(self.history_tab, "History")
        main_layout.addWidget(self.tabs)

        # Calculator Tab
        calc_layout = QVBoxLayout()
        self.calc_tab.setLayout(calc_layout)

        # Output and Light Display (single display approach)
        self.result_display = QTextEdit()
        self.result_display.setFont(QFont("Courier", 20))
        self.result_display.setReadOnly(True)
        self.result_display.setAlignment(Qt.AlignmentFlag.AlignRight)
        calc_layout.addWidget(self.result_display)

        buttons = [
            ["AC", "C", "ANS", "="],
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["0", ".", "(", ")"],
            ["+", "mod", "sqrt", "!"],
            ["sin", "cos", "tan", "log"],
            ["ln", "exp", "abs", "^"],
            ["π", "ℯ"]
        ]

        for row in buttons:
            row_layout = QHBoxLayout()
            for btn_text in row:
                button = QPushButton(btn_text)
                button.clicked.connect(self.on_button_click)
                button.setFixedHeight(50)
                button.setStyleSheet(self.get_button_style(btn_text))
                row_layout.addWidget(button)
            calc_layout.addLayout(row_layout)

        # History Tab
        self.history_display = QTextEdit()
        self.history_display.setReadOnly(True)
        self.history_tab.setLayout(QVBoxLayout())
        self.history_tab.layout().addWidget(self.history_display)

        self.setLayout(main_layout)
        self.toggle_theme()

    def get_button_style(self, text):
        if text in {"+", "-", "*", "/", "=", "sqrt", "^", "mod", "!"}:
            return "background-color: #ff9500; color: black; font-weight: bold; border-radius: 8px;"
        elif text in {"sin", "cos", "tan", "log", "ln", "exp", "abs"}:
            return "background-color: #ffcc66; color: black; font-weight: bold; border-radius: 8px;"
        elif text == "ANS":
            return "background-color: #888; color: white; font-weight: bold; border-radius: 8px;"
        elif text in {"C", "AC"}:
            return "background-color: #d32f2f; color: white; font-weight: bold; border-radius: 8px;"
        elif text in {"π", "ℯ"}:
            return "background-color: #333; color: white; font-weight: bold; border-radius: 8px;"
        else:
            return "background-color: #333; color: white; border-radius: 8px;"

    def on_button_click(self):
        sender = self.sender()
        btn_text = sender.text()
        current = self.result_display.toPlainText()

        if btn_text == "AC":
            self.result_display.clear()
        elif btn_text == "C":
            lines = current.splitlines()
            if lines:
                lines[-1] = lines[-1][:-1]
                self.result_display.setPlainText("\n".join(lines))
        elif btn_text == "=":
            self.evaluate()
        elif btn_text == "ANS":
            if self.history:
                self.result_display.append(str(self.history[-1][1]))
        elif btn_text == "sqrt":
            self.append_expression("math.sqrt(")
        elif btn_text == "!":
            self.append_expression("math.factorial(")
        elif btn_text in {"sin", "cos", "tan", "log", "ln", "exp", "abs"}:
            func_map = {
                "ln": "math.log(",
                "log": "math.log10(",
                "exp": "math.exp(",
                "abs": "abs(",
                "sin": "math.sin(",
                "cos": "math.cos(",
                "tan": "math.tan(",
            }
            self.append_expression(func_map[btn_text])
        elif btn_text == "mod":
            self.append_expression("%")
        elif btn_text == "^":
            self.append_expression("**")
        elif btn_text == "π":
            self.append_expression("math.pi")
        elif btn_text == "ℯ":
            self.append_expression("math.e")
        else:
            self.append_expression(btn_text)

    def append_expression(self, text):
        self.result_display.insertPlainText(text)

    def evaluate(self):
        expr = self.result_display.toPlainText().splitlines()
        if not expr:
            return
        try:
            expression = expr[-1]
            result = eval(expression)
            self.history.append((expression, result))
            self.result_display.append(f"= {result}")
            self.update_history()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Invalid Expression:\n{str(e)}")

    def update_history(self):
        self.history_display.clear()
        for expr, result in self.history[-50:]:
            self.history_display.append(f"{expr} = {result}")

    def toggle_theme(self):
        if self.theme_toggle.isChecked():
            self.setStyleSheet("""
                QWidget { background-color: #121212; color: white; }
                QLineEdit, QTextEdit { background-color: #1e1e1e; color: white; border: 2px solid #888; border-radius: 8px; }
                QPushButton { background-color: #333; color: white; border-radius: 8px; }
                QPushButton:hover { background-color: #666; }
                QTabBar::tab { background: #ddd; color: black; padding: 8px; border-top-left-radius: 6px; border-top-right-radius: 6px; }
                QTabBar::tab:selected { background: white; color: black; }
            """)
        else:
            self.setStyleSheet("""
                QWidget { background-color: #f0f0f0; color: black; }
                QLineEdit, QTextEdit { background-color: #fff; color: black; border: 2px solid #333; border-radius: 8px; }
                QPushButton { background-color: #ddd; color: black; border-radius: 8px; }
                QPushButton:hover { background-color: #bbb; }
                QTabBar::tab { background: #eee; color: black; padding: 8px; border-top-left-radius: 6px; border-top-right-radius: 6px; }
                QTabBar::tab:selected { background: white; color: black; }
            """)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = CalcForge()
    calc.show()
    sys.exit(app.exec())
