from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt
from register import RegisterWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login')
        self.setWindowIcon(QIcon('login.png'))
        self.setGeometry(100, 100, 300, 250)

        # Fonts
        font = QFont()
        font.setPointSize(12)

        # Widgets
        self.image = QLabel()
        pixmap = QPixmap('panda.png')
        pixmap = pixmap.scaled(175, 175, Qt.KeepAspectRatio)
        self.image.setPixmap(pixmap)
        self.image.setAlignment(Qt.AlignCenter)

        self.username_label = QLabel('Username')
        self.username_label.setFont(font)
        self.username = QLineEdit()
        self.username.setFont(font)

        self.password_label = QLabel('Password')
        self.password_label.setFont(font)
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setFont(font)

        self.login_btn = QPushButton('Login')
        self.login_btn.setFont(font)
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.setStyleSheet('''
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            padding: 5px 10px;
        ''')
        self.login_btn.clicked.connect(self.login)

        self.register_label = QLabel("Don't have an account? Register")
        self.register_label.setFont(font)

        self.register_btn = QPushButton('Register')
        self.register_btn.setFont(font)
        self.register_btn.setCursor(Qt.PointingHandCursor)
        self.register_btn.setStyleSheet('''
            background-color: #2196F3;
            color: white;
            border-radius: 5px;
            padding: 5px 10px;
        ''')
        self.register_btn.clicked.connect(self.register)

        # Layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.image)
        vbox.addWidget(self.username_label)
        vbox.addWidget(self.username)
        vbox.addWidget(self.password_label)
        vbox.addWidget(self.password)
        vbox.addStretch(1)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.login_btn)
        hbox.addStretch(1)
        vbox.addLayout(hbox)

        vbox.addWidget(self.register_label)
        vbox.addWidget(self.register_btn)
        vbox.setAlignment(Qt.AlignCenter)

        self.setLayout(vbox)

    def login(self):
        # Implement your login logic here
        username = self.username.text()
        password = self.password.text()

        if username == 'admin' and password == 'password':
            print('Login successful')
        else:
            print('Invalid username or password')

    def register(self):
        # Implement your register logic here
        # Open the register window
        self.register_window = RegisterWindow()
        self.hide()
        self.register_window.show()

if __name__ == '__main__':
    app = QApplication([])
    window = LoginWindow()
    window.show()
    app.exec_()
