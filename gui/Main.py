import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QMainWindow


class Window(QMainWindow):
    # class MainWindow(object):
    def __init__(self):
        # def setupUi(self, Window):
        super(Window, self).__init__()
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

        """
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(5, 5, 490, 155))
        self.tabWidget.setStyleSheet("")
        """
        ########
        self.horizontalLayoutWidget = QtWidgets.QWidget()
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(5, 5, 475, 120))

        self.buttonHLayout = QtWidgets.QHBoxLayout()
        self.signUpButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.signUpButton.setText("Регистрация")
        self.signUpButton.setStatusTip("Зарегистрироваться")
        self.signInButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.signInButton.setText("Авторизация")
        self.signInButton.setStatusTip("Авторизироваться")
        self.buttonHLayout.addWidget(self.signInButton)
        self.buttonHLayout.addWidget(self.signUpButton)
        #self.signInButton.clicked.connect(self.SignIn)
        #self.signUpButton.clicked.connect(self.SignUp)

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


def run():
    app = QtWidgets.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())