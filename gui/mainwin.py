import sys

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QStackedLayout

import pymysql as mdb

from gui.signin import SignInWindow
from gui.signup import SignUpWindow

mdb.install_as_MySQLdb()



class MainWindow(QMainWindow):

    def __init__(self):

        super(MainWindow, self).__init__()
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
        #self.widsLayout = QStackedLayout(self)

        ########
        #self.wid1 = QtWidgets.QWidget(self)
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 481, 151))

        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(10)

        self.hostKey = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.hostKey, 0, 1, 1, 1)

        self.userLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.userLabel.setFont(font)
        self.userLabel.setText("user")
        self.gridLayout.addWidget(self.userLabel, 1, 0, 1, 1)

        self.pwdLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pwdLabel.setFont(font)
        self.pwdLabel.setText("password")
        self.gridLayout.addWidget(self.pwdLabel, 2, 0, 1, 1)

        self.hostLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.hostLabel.setFont(font)
        self.hostLabel.setText("host")
        self.gridLayout.addWidget(self.hostLabel, 0, 0, 1, 1)

        self.dbLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.dbLabel.setFont(font)
        self.dbLabel.setText("data base")
        self.gridLayout.addWidget(self.dbLabel, 3, 0, 1, 1)

        self.userKey = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.userKey, 1, 1, 1, 1)

        self.dbKey = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.dbKey, 3, 1, 1, 1)

        self.pwdKey = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.pwdKey.setEchoMode(QtWidgets.QLineEdit.Password)
        self.gridLayout.addWidget(self.pwdKey, 2, 1, 1, 1)

        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.conButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.conButton.setText("Соединение")
        self.conButton.setStatusTip("Соединиться с БД")
        self.conButton.setEnabled(True)
        self.buttonLayout.addWidget(self.conButton)

        self.signUpButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.signUpButton.setText("Регистрация")
        self.signUpButton.setStatusTip("Зарегистрироваться")
        self.buttonLayout.addWidget(self.signUpButton)

        self.signInButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.signInButton.setText("Авторизация")
        self.signInButton.setStatusTip("Авторизироваться")
        self.buttonLayout.addWidget(self.signInButton)

        self.gridLayout.addLayout(self.buttonLayout, 5, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 4)

        self.conButton.clicked.connect(self.connectDB)
        self.signUpButton.clicked.connect(self.regOpen)
        self.signInButton.clicked.connect(self.autoOpen)

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

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Выход', "Вы действительно хотите покинуть программу?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:

            event.accept()
        else:
            event.ignore()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def about(self):
        QMessageBox.about(self, 'О программе',
                          "* Регистрация на сервере с БД\n* Реализация метода аутентификации слово-вызов. Сеансовый ключ по Соловею-Штрассену\n* Реализация алгоритма Диффи-Хеллмана\n* Реализация метода RC4\n*")

    def help(self):
        QMessageBox.information(self, 'Помощь', "??")

    def connectDB(self):

        myhost = self.hostKey.text()
        myuser= self.userKey.text()
        mypassword = self.pwdKey.text()
        mydb = self.dbKey.text()

        try:
            db = mdb.connect(host=myhost, user=myuser, password=mypassword, db=mydb)
            QMessageBox.about(self, 'Соединение', 'Вы подключены:)')
        except mdb.Error as e:
            QMessageBox.about(self, 'Соединение', 'Ошибка подключения!')

    def regOpen(self):
        self.open = SignUpWindow()

    def autoOpen(self):
        self.open= SignInWindow()

def run():
    app = QtWidgets.QApplication(sys.argv)
    GUI = MainWindow()
    sys.exit(app.exec_())