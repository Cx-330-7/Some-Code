from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QStringListModel
import pymysql


class Ui_MainWindow(QWidget):
    def __init__(self, name, userId):
        super().__init__()
        self.username = name
        self.userId = userId
        self.list = []
        self.notList = []
        db = pymysql.connect(host='localhost',
                             user='root',
                             password='Zjy9201141217',
                             database='test')
        cursor1 = db.cursor()
        ver_sql = "SELECT COUNT(userId) FROM userAndphoto"
        cursor1.execute(ver_sql)
        num = cursor1.fetchall()
        self.allClerk = num[0][0]
        cursor2 = db.cursor()
        has_sql = "SELECT COUNT(userId) FROM userAndphoto WHERE pc = 1"
        cursor2.execute(has_sql)
        has_num = cursor2.fetchall()
        self.has = has_num[0][0]
        self.not_has = self.allClerk - self.has
        cursor3 = db.cursor()
        whoNot_sql = "SELECT name FROM userAndphoto WHERE pc = 0"
        cursor3.execute(whoNot_sql)
        whoNot_list = cursor3.fetchall()
        for i in range(len(whoNot_list)):
            self.list.append(whoNot_list[i][0])
        cursor4 = db.cursor()
        whoHas_sql = "SELECT name FROM userAndphoto WHERE pc = 1"
        cursor4.execute(whoHas_sql)
        whoHas_list = cursor4.fetchall()
        for i in range(len(whoHas_list)):
            self.notList.append(whoHas_list[i][0])
        db.close()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(776, 410)
        MainWindow.setMinimumSize(QtCore.QSize(776, 410))
        MainWindow.setMaximumSize(QtCore.QSize(776, 410))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 20, 341, 31))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.Time = QtWidgets.QLCDNumber(self.centralwidget)
        self.Time.setGeometry(QtCore.QRect(400, 20, 131, 31))
        self.Time.setObjectName("Time")
        self.Time.setDigitCount(8)  # add
        timer = QtCore.QTimer(MainWindow)  # add
        timer.timeout.connect(self.showtime_slot)  # 槽函数showtime_slot/showtime_slot2
        timer.start(0)  # add
        self.name = QtWidgets.QLabel(self.centralwidget)
        self.name.setGeometry(QtCore.QRect(650, 30, 60, 16))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.name.setFont(font)
        self.name.setText("")
        self.name.setObjectName("name")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(570, 30, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 90, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(23)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 170, 81, 41))
        font = QtGui.QFont()
        font.setPointSize(23)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(20, 250, 81, 41))
        font = QtGui.QFont()
        font.setPointSize(23)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(140, 100, 60, 21))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.label_6.setFont(font)
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(140, 180, 41, 21))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.label_7.setFont(font)
        self.label_7.setText("")
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(140, 260, 31, 21))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.label_8.setFont(font)
        self.label_8.setText("")
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(10, 20, 31, 31))
        self.label_9.setStyleSheet("background-image:url(\"/Users/zhengjunyuan/PycharmProjects/课程设计/管理.png\")")
        self.label_9.setText("")
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(170, 180, 31, 31))
        self.label_10.setStyleSheet("background-image:url(\"/Users/zhengjunyuan/PycharmProjects/课程设计/勾.png\")")
        self.label_10.setText("")
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(170, 260, 29, 29))
        self.label_11.setStyleSheet("background-image:url(\"/Users/zhengjunyuan/PycharmProjects/课程设计/叉叉.png\")")
        self.label_11.setText("")
        self.label_11.setObjectName("label_11")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(570, 120, 151, 61))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(570, 220, 151, 61))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(250, 100, 120, 201))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 118, 1000))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(118, 1000))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.listView = QtWidgets.QListView(self.scrollAreaWidgetContents)  # dd
        self.listView.setGeometry(QtCore.QRect(0, 0, 121, 1000))
        self.listView.setMinimumSize(QtCore.QSize(121, 1000))
        self.listView.setObjectName("listView")
        listModel = QStringListModel()
        listModel.setStringList(self.notList)
        self.listView.setModel(listModel)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scrollArea_2 = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea_2.setGeometry(QtCore.QRect(400, 100, 120, 201))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 118, 1000))
        self.scrollAreaWidgetContents_2.setMinimumSize(QtCore.QSize(118, 1000))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.listView_2 = QtWidgets.QListView(self.scrollAreaWidgetContents_2)
        self.listView_2.setGeometry(QtCore.QRect(0, 0, 121, 1000))
        self.listView_2.setMinimumSize(QtCore.QSize(121, 1000))
        self.listView_2.setObjectName("listView_2")
        listModel = QStringListModel()
        listModel.setStringList(self.list)
        self.listView_2.setModel(listModel)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(250, 80, 60, 16))
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(400, 80, 60, 16))
        self.label_13.setObjectName("label_13")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 776, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "人脸识别自动考勤后台管理系统"))
        self.label.setText(_translate("MainWindow", "人脸识别自动考勤后台管理系统"))
        self.label_3.setText(_translate("MainWindow", "管理员："))
        self.label_2.setText(_translate("MainWindow", "在职人员:"))
        self.label_4.setText(_translate("MainWindow", "已打卡:"))
        self.label_5.setText(_translate("MainWindow", "未打卡:"))
        self.pushButton.setText(_translate("MainWindow", "刷新"))
        self.pushButton_2.setText(_translate("MainWindow", "退出"))
        self.pushButton_2.clicked.connect(lambda: self.exit(MainWindow))
        self.label_12.setText(_translate("MainWindow", "已打卡"))
        self.label_13.setText(_translate("MainWindow", "未打卡"))
        self.label_6.setText(_translate("MainWindow", "{}".format(self.allClerk)))
        self.label_7.setText(_translate("MainWindow", "{}".format(self.has)))
        self.label_8.setText(_translate("MainWindow", "{}".format(self.not_has)))
        self.name.setText(_translate("MainWindow", self.username))
        self.pushButton.clicked.connect(lambda: self.flesh())

    def showtime_slot(self):
        time0 = QtCore.QDateTime.currentDateTime()
        str_time = time0.toString('yyyy-mm-dd hh:mm:ss')
        self.Time.display(str_time)

    def exit(self, MainWindow):
        MainWindow.close()

    def flesh(self):
        self.list = []
        self.notList = []
        _translate = QtCore.QCoreApplication.translate
        db = pymysql.connect(host='localhost',
                             user='root',
                             password='Zjy9201141217',
                             database='test')
        cursor1 = db.cursor()
        ver_sql = "SELECT COUNT(userId) FROM userAndphoto"
        cursor1.execute(ver_sql)
        num = cursor1.fetchall()
        self.allClerk = num[0][0]
        cursor2 = db.cursor()
        has_sql = "SELECT COUNT(userId) FROM userAndphoto WHERE pc = 1"
        cursor2.execute(has_sql)
        has_num = cursor2.fetchall()
        self.has = has_num[0][0]
        self.not_has = self.allClerk - self.has
        cursor3 = db.cursor()
        whoNot_sql = "SELECT name FROM userAndphoto WHERE pc = 0"
        cursor3.execute(whoNot_sql)
        whoNot_list = cursor3.fetchall()
        for i in range(len(whoNot_list)):
            self.list.append(whoNot_list[i][0])
        cursor4 = db.cursor()
        whoHas_sql = "SELECT name FROM userAndphoto WHERE pc = 1"
        cursor4.execute(whoHas_sql)
        whoHas_list = cursor4.fetchall()
        for i in range(len(whoHas_list)):
            self.notList.append(whoHas_list[i][0])
        self.label_6.setText(_translate("MainWindow", "{}".format(self.allClerk)))
        self.label_7.setText(_translate("MainWindow", "{}".format(self.has)))
        self.label_8.setText(_translate("MainWindow", "{}".format(self.not_has)))
        listModel = QStringListModel()
        listModel.setStringList(self.notList)
        self.listView.setModel(listModel)
        listModel = QStringListModel()
        listModel.setStringList(self.list)
        self.listView_2.setModel(listModel)
        db.close()
