from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QDesktopWidget
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt, QUrl

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Register')
        self.setWindowIcon(QIcon('register.png'))
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

        self.image = QLabel()
        pixmap = QPixmap('panda.png')
        pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio)
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

        self.confirm_password_label = QLabel('Confirm Password')
        self.confirm_password_label.setFont(font)
        self.confirm_password = QLineEdit()
        self.confirm_password.setEchoMode(QLineEdit.Password)
        self.confirm_password.setFont(font)

        self.register_btn = QPushButton('Register')
        self.register_btn.setFont(font)
        self.register_btn.setCursor(Qt.PointingHandCursor)
        self.register_btn.setStyleSheet('''
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            padding: 5px 10px;
        ''')
        self.register_btn.clicked.connect(self.register)

        self.login_label = QLabel('Already have an account? ')
        self.login_label.setFont(font)

        self.login_link = QLabel('Login')
        self.login_link.setFont(font)
        self.login_link.setCursor(Qt.PointingHandCursor)
        self.login_link.setStyleSheet('color: blue;')
        self.login_link.setOpenExternalLinks(True)
        self.login_link.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.login_link.linkActivated.connect(self.login)

        # Layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.image)
        vbox.addWidget(self.username_label)
        vbox.addWidget(self.username)
        vbox.addWidget(self.password_label)
        vbox.addWidget(self.password)
        vbox.addWidget(self.confirm_password_label)
        vbox.addWidget(self.confirm_password)
        vbox.addStretch(1)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.register_btn)
        hbox.addStretch(1)
        vbox.addLayout(hbox)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.login_label)
        hbox2.addWidget(self.login_link)
        hbox2.addStretch(1)
        vbox.addLayout(hbox2)

        vbox.setAlignment(Qt.AlignCenter)

        self.setLayout(vbox)
        self.center()

    def center(self):
        # Center the window on the screen
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def register(self):
        # Implement your register logic here
        username = self.username.text()
        password = self.password.text()
        confirm_password = self.confirm_password.text()

        if password != confirm_password:
            print('Passwords do not match')
        else:
            print('Registration successful')

    def login(self):
        # Implement your login logic here
        print('Login link clicked')

if __name__ == '__main__':
    app = QApplication([])
    window = RegisterWindow()
    window.show()
    app.exec_()
