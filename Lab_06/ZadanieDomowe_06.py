import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget,
                             QLineEdit, QGridLayout, QMessageBox, QComboBox)
from calculator_logic import CalculatorLogic

class CalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.logic = CalculatorLogic()
        self.current_input = ""
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Calculator")
        self.setGeometry(100, 100, 300, 400)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.main_layout = QVBoxLayout(central_widget)

        self.display = QLineEdit(self)
        self.display.setReadOnly(True)
        self.display.setFixedHeight(50)
        self.main_layout.addWidget(self.display)

        self.mode_selector = QComboBox(self)
        self.mode_selector.addItems(["Decimal", "Binary", "Hexadecimal"])
        self.mode_selector.currentTextChanged.connect(self.update_mode)
        self.main_layout.addWidget(self.mode_selector)

        self.buttons_layout = QGridLayout()
        self.main_layout.addLayout(self.buttons_layout)

        self.create_decimal_buttons()

    def create_decimal_buttons(self):
        buttons = [
            ('7', '8', '9', '/', '√'),
            ('4', '5', '6', '*', 'CE'),
            ('1', '2', '3', '-', ' C '),
            ('.', '0', '^', '+', '='),
        ]
        self.add_buttons(buttons)

    def create_binary_buttons(self):
        buttons = [
            ('0', '1'),
            ('+', '-', '*'),
            (' C ', 'CE', '='),
        ]
        self.add_buttons(buttons)

    def create_hexadecimal_buttons(self):
        buttons = [
            ('A', '*', 'CE', ' C '),
            ('B', '7', '8', '9'),
            ('C', '4', '5', '6'),
            ('D', '1', '2', '3'),
            ('E', '-', '0', '+'),
            ('F', '', '', '='),
        ]
        self.add_buttons(buttons)

    def add_buttons(self, buttons):
        self._clear_existing_buttons()

        for row_index, row in enumerate(buttons):
            for col_index, button_label in enumerate(row):
                if button_label:
                    self._create_and_add_button(button_label, row_index, col_index)

    def _clear_existing_buttons(self):
        for i in reversed(range(self.buttons_layout.count())):
            widget = self.buttons_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

    def _create_and_add_button(self, label, row, column):
        button = QPushButton(label)
        button.setFixedSize(50, 50)
        button.clicked.connect(self.button_pressed)
        self.buttons_layout.addWidget(button, row, column)

    def update_mode(self):
        mode = self.mode_selector.currentText()
        match mode:
            case "Decimal":
                self.logic.current_system = 10
                self.create_decimal_buttons()
            case "Binary":
                self.logic.current_system = 2
                self.create_binary_buttons()
            case "Hexadecimal":
                self.logic.current_system = 16
                self.create_hexadecimal_buttons()
        try:
            if self.current_input:
                self.current_input = self.logic.convert_number( self.current_input, self.logic.previous_system,
                                                                self.logic.current_system)
                self.display.setText(self.current_input)
                self.logic.previous_system = self.logic.current_system
            else:
                self.display.clear()
        except ValueError:
            self.display.clear()
            self.current_input = ""

    def button_pressed(self):
        sender = self.sender()
        text = sender.text()

        match text:
            case "=":
                try:
                    result = self.logic.evaluate_expression(self.current_input)
                    self.display.setText(result)
                    self.current_input = result
                except ValueError as e:
                    self.show_error_message(str(e))
            case " C ":
                self.current_input = ""
                self.display.clear()
            case "CE":
                self.current_input = self.current_input[:-1]
                self.display.setText(self.current_input)
            case _:
                self.current_input += text
                self.display.setText(self.current_input)

    def show_error_message(self, message):
        error_box = QMessageBox(self)
        error_box.setIcon(QMessageBox.Warning)
        error_box.setText(message)
        error_box.setWindowTitle("Error")
        error_box.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalculatorApp()
    window.show()
    sys.exit(app.exec_())
