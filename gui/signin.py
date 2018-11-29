import sys


from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QStackedLayout

from prog.SSPT import generatePrime
from prog.hashing import computeMD5hash
from Crypto.Util import number

import pymysql as mdb

class SignInWindow(QMainWindow):
    # class MainWindow(object):
    def __init__(self):
        # def setupUi(self, Window):
        super(SignInWindow, self).__init__()
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
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 30, 481, 81))

        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)

        self.passwordLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.passwordLabel.setFont(font)
        self.passwordLabel.setText("Пароль")
        self.gridLayout_2.addWidget(self.passwordLabel, 1, 0, 1, 1)

        self.loginKey = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.gridLayout_2.addWidget(self.loginKey, 0, 1, 1, 1)

        self.loginLabel = QtWidgets.QLabel(self.gridLayoutWidget)

        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.loginLabel.setFont(font)
        self.loginLabel.setText("Логин")
        self.gridLayout_2.addWidget(self.loginLabel, 0, 0, 1, 1)

        self.passKey = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.passKey.setEchoMode(QtWidgets.QLineEdit.Password)
        self.gridLayout_2.addWidget(self.passKey, 1, 1, 1, 1)

        self.titleLabel = QtWidgets.QLabel(self.centralwidget)
        self.titleLabel.setGeometry(QtCore.QRect(180, 0, 131, 20))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(True)
        font.setWeight(75)
        self.titleLabel.setFont(font)
        self.titleLabel.setText("Авторизация")

        ######
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(250, 120, 241, 31))
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(10)

        self.okButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.okButton.setText("OK")
        self.horizontalLayout_2.addWidget(self.okButton)

        self.cancelButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.cancelButton.setText("Отмена")
        self.horizontalLayout_2.addWidget(self.cancelButton)

        self.okButton.clicked.connect(self.Authorization)
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

    def Authorization(self):
        mylogin = self.loginKey.text()
        #mypassword = self.passKey.text()

        mymd5 = computeMD5hash(self.passKey.text())
        #print(type(mymd5))
        #check_user

        con = mdb.connect(host='localhost',
                          user='root',
                          password='root',
                          db='ibks',
                          autocommit=True)
        try:
            with con.cursor() as cur:

                cur.execute("SELECT password from users WHERE login=%s",mylogin)
                result = cur.fetchone()
                #print(result[0],type(result[0]))

                if result!=None:
                    key = number.getPrime(128)
                    print(key)
                    userhash = computeMD5hash(str(int(mymd5, 16) + key)) #относитеьно клиента
                    dbhash =computeMD5hash(str(int(result[0], 16) + key)) #относительно сервера
                    #print(userhash, type(userhash))
                    #print(dbhash, type(dbhash))

                    if userhash==dbhash:
                        QMessageBox.about(self, 'Авторизация',"Успешно!")
                    else:
                        QMessageBox.about(self, 'Авторизация', "Неверный пароль!")
                else:
                    QMessageBox.about(self, 'Авторизация', "Пользователь не найден")
                #cur.close()
        except mdb.Error as e:
            QMessageBox.about(self, 'Авторизация', 'Ошибка!\n'+str(e.args))
            con.close()






if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    GUI = SignInWindow()
    sys.exit(app.exec_())