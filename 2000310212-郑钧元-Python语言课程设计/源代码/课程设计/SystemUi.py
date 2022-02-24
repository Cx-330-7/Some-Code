from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QMessageBox
import base64
import requests
import json
import pymysql
import cv2
import uuid


class Ui_MainWindow(QWidget):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(621, 241)
        MainWindow.setMinimumSize(QtCore.QSize(621, 241))
        MainWindow.setMaximumSize(QtCore.QSize(621, 241))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("考勤排班.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(40, 20, 240, 33))
        font = QtGui.QFont()
        font.setPointSize(23)
        self.title.setFont(font)
        self.title.setObjectName("title")
        self.actionButton = QtWidgets.QPushButton(self.centralwidget)
        self.actionButton.setGeometry(QtCore.QRect(10, 130, 151, 61))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.actionButton.setFont(font)
        self.actionButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.actionButton.setObjectName("actionButton")
        self.calendar = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendar.setGeometry(QtCore.QRect(330, 0, 291, 221))
        self.calendar.setObjectName("calendar")
        self.Time = QtWidgets.QLCDNumber(self.centralwidget)
        self.Time.setGeometry(QtCore.QRect(90, 70, 131, 41))
        self.Time.setObjectName("Time")
        self.Time.setDigitCount(8)  # add
        timer = QtCore.QTimer(MainWindow)  # add
        timer.timeout.connect(self.showtime_slot)  # 槽函数showtime_slot/showtime_slot2
        timer.start(0)  # add
        self.actionButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.actionButton_2.setGeometry(QtCore.QRect(170, 130, 151, 61))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.actionButton_2.setFont(font)
        self.actionButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.actionButton_2.setObjectName("actionButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 621, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "人脸识别自动考勤系统"))
        self.title.setText(_translate("MainWindow", "人脸识别自动考勤系统"))
        self.actionButton.setText(_translate("MainWindow", "点击签到"))
        self.actionButton_2.setText(_translate("MainWindow", "添加用户"))
        self.actionButton.clicked.connect(lambda: self.search(self.take_photo()))

    def showtime_slot(self):
        time0 = QtCore.QDateTime.currentDateTime()
        str_time = time0.toString('yyyy-mm-dd hh:mm:ss')
        self.Time.display(str_time)

    def search(self, url):
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
        print(result)
        # print(result['result']['user_list']['score'])
        if result['result']['user_list'][0]['score'] < 80:
            QMessageBox.warning(self, "警告", "您还没有注册！", QMessageBox.Cancel)
        elif result['result'] is None:
            QMessageBox.warning(self, "提示", "未检测到人脸,请重新检测!", QMessageBox.Cancel)
        else:
            userId = result['result']['user_list'][0]['user_id']
            db = pymysql.connect(host='localhost',
                                 user='root',
                                 password='Zjy9201141217',
                                 database='test')
            cursor = db.cursor()
            sql = "SELECT name,pc FROM userAndphoto WHERE userId ='" + userId + "' "
            cursor.execute(sql)
            data = cursor.fetchone()
            if data[1] == 1:
                QMessageBox.warning(self, "提示", data[0] + "，您今天已经打过卡了", QMessageBox.Cancel)
            else:
                QMessageBox.information(self, "打卡成功", data[0] + "打卡成功", QMessageBox.Yes)
                try:
                    update_sql = "update userAndphoto set pc = 1 where name = '" + data[0] + "' "
                    cursor.execute(update_sql)
                    db.commit()
                except:
                    db.rollback()
            db.close()

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
