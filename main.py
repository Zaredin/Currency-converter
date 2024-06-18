import sys
import requests
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox
from PyQt6.QtCore import QFile, QTextStream, Qt

API_KEY = 'your_api_key_here'  # Replace with your actual API key

class CurrencyConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.apply_stylesheet()

    def initUI(self):
        self.setWindowTitle('Currency Converter')
        self.setGeometry(100, 100, 500, 200)
        
        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        bottom_layout = QVBoxLayout()

        
        self.amount_label = QLabel('Amount:', self)
        main_layout.addWidget(self.amount_label)

        self.amount_input = QLineEdit(self)
        main_layout.addWidget(self.amount_input)


        self.from_currency_button = QPushButton('USD', self)
        self.from_currency_button.clicked.connect(self.show_from_currency_menu)
        top_layout.addWidget(self.from_currency_button)

        self.from_currency = QComboBox(self)
        self.from_currency.setVisible(False)  
        self.from_currency.currentIndexChanged.connect(self.update_from_currency_button)
        top_layout.addWidget(self.from_currency)

        
        self.cur_exchange_label = QLabel('From/To', self)
        self.cur_exchange_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_layout.addWidget(self.cur_exchange_label)

        self.to_currency_button = QPushButton('EUR', self)
        self.to_currency_button.clicked.connect(self.show_to_currency_menu)
        top_layout.addWidget(self.to_currency_button)

        self.to_currency = QComboBox(self)
        self.to_currency.setVisible(False)  
        self.to_currency.currentIndexChanged.connect(self.update_to_currency_button)
        top_layout.addWidget(self.to_currency)

        main_layout.addLayout(top_layout)

        
        self.convert_button = QPushButton('Convert', self)
        self.convert_button.clicked.connect(self.convert_currency)
        bottom_layout.addWidget(self.convert_button)

        
        self.result_label = QLabel('', self)
        bottom_layout.addWidget(self.result_label)

        main_layout.addLayout(bottom_layout)
        self.setLayout(main_layout)
        
        self.load_currencies()

    def load_currencies(self):
        try:
            url = f"https://open.er-api.com/v6/latest/USD"
            response = requests.get(url)
            data = response.json()
            
            if data['result'] == 'success':
                currencies = data['rates'].keys()
                self.from_currency.addItems(currencies)
                self.to_currency.addItems(currencies)
            else:
                self.show_error("Failed to load currencies.")
        except Exception as e:
            self.show_error(str(e))

    def convert_currency(self):
        try:
            amount = float(self.amount_input.text())
            from_currency = self.from_currency.currentText()
            to_currency = self.to_currency.currentText()
            
            rate = self.get_exchange_rate(from_currency, to_currency)
            converted_amount = amount * rate
            
            self.result_label.setText(f'{amount} {from_currency} = {converted_amount:.2f} {to_currency}')
        except ValueError:
            self.show_error("Please enter a valid amount.")
        except Exception as e:
            self.show_error(str(e))

    def get_exchange_rate(self, from_currency, to_currency):
        url = f"https://open.er-api.com/v6/latest/{from_currency}"
        response = requests.get(url)
        data = response.json()
        
        if data['result'] == 'success':
            return data['rates'][to_currency]
        else:
            self.show_error("Failed to fetch exchange rate.")
            return 1

    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)

    def show_from_currency_menu(self):
        self.from_currency.showPopup()

    def show_to_currency_menu(self):
        self.to_currency.showPopup()

    def update_from_currency_button(self):
        self.from_currency_button.setText(self.from_currency.currentText())

    def update_to_currency_button(self):
        self.to_currency_button.setText(self.to_currency.currentText())

    def apply_stylesheet(self):
        file = QFile("styles.css")
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    converter = CurrencyConverter()
    converter.show()
    sys.exit(app.exec())