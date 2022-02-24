from PyQt5 import QtCore, QtGui, QtWidgets
import base64
import requests
import json
import pymysql
from PyQt5.QtWidgets import QWidget, QMessageBox, QMainWindow
import cv2
import uuid
import ManageMainUi as mmu


class Ui_MainWindow(QWidget):
    name = ''

    def setupUi(self, MainWindow, MainWindow2):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(530, 344)
        MainWindow.setMinimumSize(QtCore.QSize(530, 244))
        MainWindow.setMaximumSize(QtCore.QSize(530, 344))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(100, 20, 321, 31))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(200, 80, 121, 121))
        self.label_2.setStyleSheet("background-image:url(\"/Users/zhengjunyuan/PycharmProjects/课程设计/Manage.png\")")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(170, 230, 191, 61))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.pushButton.setFont(font)
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 530, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow, MainWindow2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow, MainWindow2):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "人脸识别自动考勤后台管理系统"))
        self.label.setText(_translate("MainWindow", "人脸识别自动考勤后台管理系统"))
        self.pushButton.setText(_translate("MainWindow", "登录"))
        self.pushButton.clicked.connect(lambda: self.login(self.take_photo(), MainWindow, MainWindow2))

    def login(self, url, QMainWindow_1, QMainWindow_2):
        client_id = "N5GHjXHSFQHtVM0yrHWSK1o4"
        client_secret = "nIDUqoQq3446Z15Gz8A8d5K7mai1b4ve"
        token_url = "https://aip.baidubce.com/oauth/2.0/token"
        host = f"{token_url}?grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}"
        response = requests.get(host)
        access_token = response.json().get("access_token")
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/search"
        with open(url, 'rb') as f:
            image = base64.b64encode(f.read())
        body = {
            "image": image,
            "image_type": "BASE64",
            "group_id_list": "N1",
            "quality_control": "NONE",
            "liveness_control": "NONE",
        }

        headers = {"Content-Type": "application/json"}
        request_url = f"{request_url}?access_token={access_token}"
        response = requests.post(request_url, headers=headers, data=body)
        result = json.loads(response.content.decode("UTF-8"))
        if result['result'] is None:
            QMessageBox.warning(self, "提示", "未检测到人脸,请重新检测!", QMessageBox.Cancel)
        else:
            userId = result['result']['user_list'][0]['user_id']
            db = pymysql.connect(host='localhost',
                                 user='root',
                                 password='Zjy9201141217',
                                 database='test')
            cursor = db.cursor()
            sql = "SELECT name,role FROM userAndphoto WHERE userId ='" + userId + "' "
            cursor.execute(sql)
            data = cursor.fetchone()
            if data[1] != 1:
                QMessageBox.warning(self, "警告", "您还不是管理员，无法登录", QMessageBox.Cancel)
            else:
                QMainWindow_1.close()
                self.name = data[0]
                ui = mmu.Ui_MainWindow(self.name,userId)
                ui.setupUi(QMainWindow_2)
                QMainWindow_2.show()

    def take_photo(self):
        cap = cv2.VideoCapture(0)
        url_pre = "/Users/zhengjunyuan/Desktop/face_test/"
        url_aft = str(uuid.uuid4()) + '.jpeg'
        url = url_pre + url_aft
        while True:
            ret, frame = cap.read()
            cv2.imshow("FaceRecognition", frame)
            if cv2.waitKey(1) & 0xFF == ord('p'):
                cv2.imwrite(url, frame)
                break
        cap.release()
        cv2.destroyAllWindows()
        return url
