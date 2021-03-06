import sys

import pymysql
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QMainWindow

# from gui.mainwin import MainWindow
from prog.hashing import computeMD5hash


class SignUpWindow(QMainWindow):
    def __init__(self):
        super(SignUpWindow, self).__init__()
        self.setFixedSize(500, 200)
        self.setWindowTitle('Информационная безопасность компьютерных сетей')
        self.setWindowIcon(QIcon('icons/lock3.png'))

        self.init_Action()
        self.init_Content()
        self.init_StatusBar()
        self.init_Menu()
        self.set_Actions2Menu()
        self.set_Actions2StatusBar()
        self.set_Triggers2Actions()
        self.show()

    def init_Content(self):
        self.centralwidget = QtWidgets.QWidget(self)

        ########
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 30, 481, 91))

        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)

        self.loginKey = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.gridLayout_2.addWidget(self.loginKey, 0, 1, 1, 1)

        self.loginLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.loginLabel.setFont(font)
        self.loginLabel.setText("Логин")
        self.gridLayout_2.addWidget(self.loginLabel, 0, 0, 1, 1)

        self.passwordLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.passwordLabel.setFont(font)
        self.passwordLabel.setText("Пароль")
        self.gridLayout_2.addWidget(self.passwordLabel, 1, 0, 1, 1)

        self.licenseBox = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.licenseBox.setText("Согласен на обработку персональных данных")
        self.gridLayout_2.addWidget(self.licenseBox, 2, 1, 1, 1)

        self.licenseLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.licenseLabel.setFont(font)
        self.gridLayout_2.addWidget(self.licenseLabel, 2, 0, 1, 1)

        self.passKey = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.passKey.setEchoMode(QtWidgets.QLineEdit.Password)
        self.gridLayout_2.addWidget(self.passKey, 1, 1, 1, 1)

        self.titleLabel = QtWidgets.QLabel(self.centralwidget)
        self.titleLabel.setGeometry(QtCore.QRect(180, 0, 121, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(True)
        font.setWeight(75)
        self.titleLabel.setFont(font)
        self.titleLabel.setText("РЕГИСТРАЦИЯ")

        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(251, 130, 241, 31))

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(10)

        self.okButton = QtWidgets.QPushButton(self.layoutWidget)
        self.okButton.setText("OK")
        self.horizontalLayout_2.addWidget(self.okButton)

        self.cancelButton = QtWidgets.QPushButton(self.layoutWidget)
        self.cancelButton.setText("Отмена")
        self.horizontalLayout_2.addWidget(self.cancelButton)

        self.okButton.clicked.connect(self.Reg)
        self.cancelButton.clicked.connect(self.close)

        self.setCentralWidget(self.centralwidget)

    def init_StatusBar(self):
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setSizeGripEnabled(True)
        self.setStatusBar(self.statusbar)

    def init_Action(self):
        self.ExitAction = QtWidgets.QAction(QIcon('icons/exit.png'), "Выход", self)
        self.HelpAction = QtWidgets.QAction(QIcon('icons/question.png'), "Помощь", self)
        self.AboutAction = QtWidgets.QAction(QIcon('icons/about.png'), "О программе", self)

        self.ExitAction.setShortcut('Ctrl+Q')
        self.HelpAction.setShortcut('Ctrl+H')
        self.AboutAction.setShortcut('Ctrl+I')

    def set_Actions2StatusBar(self):

        self.ExitAction.setStatusTip('Выход')
        self.HelpAction.setStatusTip('Помощь')
        self.AboutAction.setStatusTip('О программе')

    def set_Triggers2Actions(self):
        self.ExitAction.triggered.connect(self.close)
        self.HelpAction.triggered.connect(self.help)
        self.AboutAction.triggered.connect(self.about)

    def init_Menu(self):
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 500, 20))
        self.fileMenu = QtWidgets.QMenu(self.menubar)
        self.helpMenu = QtWidgets.QMenu(self.menubar)
        self.fileMenu.setTitle("Файл ")
        self.helpMenu.setTitle("Справка")
        self.menubar.addAction(self.fileMenu.menuAction())
        self.menubar.addAction(self.helpMenu.menuAction())
        self.setMenuBar(self.menubar)

    def set_Actions2Menu(self):

        self.fileMenu.addAction(self.ExitAction)
        self.helpMenu.addAction(self.HelpAction)
        self.helpMenu.addAction(self.AboutAction)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def about(self):
        QMessageBox.about(self, 'О программе',
                          "* Регистрация на сервере с БД\n* Реализация метода аутентификации слово-вызов. Сеансовый ключ по Соловею-Штрассену\n* Реализация алгоритма Диффи-Хеллмана\n* Реализация метода RC4\n*")

    def help(self):
        QMessageBox.information(self, 'Помощь', "??")

    def Reg(self):
        mylogin = self.loginKey.text()
        mypassword = self.passKey.text()
        mymd5 = computeMD5hash(mypassword)
        print(type(mylogin),type(mymd5))

        con = pymysql.connect(host='localhost',
                              user='root',
                              password='root',
                              port=3306,
                              db='ibks',
                              autocommit=True)

        try:
            with con.cursor() as cur:
                cur.execute("SELECT login FROM users WHERE login=%s", mylogin)
                result = cur.fetchone()
                print(result)
                if result == None:

                    cur.execute("INSERT INTO users (login, password) VALUES (%s, %s)",(mylogin, mymd5))
                    QMessageBox.about(self, 'Регистрация', 'Вы успешно зарегистрированы!')

                else:
                    QMessageBox.about(self, 'Регистрация', 'Такой пользователь уже существует!')

                #cur.close()
        except pymysql.Error as e:
            QMessageBox.about(self, 'Регистрация', 'Ошибка!\n'+str(e.args))
        con.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    GUI = SignUpWindow()
    sys.exit(app.exec_())
