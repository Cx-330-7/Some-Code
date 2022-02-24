from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QWidget
import cv2
import uuid
import base64
import requests
import json
import pymysql


class Ui_MainWindow(QWidget):
    name = ''
    userId = ''

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(479, 282)
        MainWindow.setMinimumSize(QtCore.QSize(479, 282))
        MainWindow.setMaximumSize(QtCore.QSize(479, 282))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../PycharmProjects/课程设计/考勤排班.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(190, 10, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(23)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(110, 70, 60, 16))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(90, 120, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(50, 170, 161, 61))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.pushButton.setFont(font)
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(260, 170, 161, 61))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setObjectName("pushButton_2")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(170, 60, 171, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(170, 110, 171, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 479, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "添加用户"))
        self.label.setText(_translate("MainWindow", "添加用户"))
        self.label_2.setText(_translate("MainWindow", "姓名："))
        self.label_3.setText(_translate("MainWindow", "UserId："))
        self.pushButton.setText(_translate("MainWindow", "录入人脸"))
        self.pushButton_2.setText(_translate("MainWindow", "返回系统"))
        self.pushButton.clicked.connect(lambda: self.register(self.take_photo(), self.userId, self.name))

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
        self.name = self.lineEdit.text()
        self.userId = self.lineEdit_2.text()
        return url

    def register(self, url, userId, name):
        db = pymysql.connect(host='localhost',
                             user='root',
                             password='Zjy9201141217',
                             database='test')
        cursor = db.cursor()
        ver_sql = "SELECT name FROM userAndphoto WHERE userId = '" + userId + "'"
        cursor.execute(ver_sql)
        nameList = cursor.fetchall()
        if len(nameList) != 0:
            if nameList[0][0] != name:
                QMessageBox.warning(self, "警告", "该用户ID已被占用，请更换！", QMessageBox.Cancel)
                return
        client_id = "N5GHjXHSFQHtVM0yrHWSK1o4"
        client_secret = "nIDUqoQq3446Z15Gz8A8d5K7mai1b4ve"
        token_url = "https://aip.baidubce.com/oauth/2.0/token"
        host = f"{token_url}?grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}"
        response = requests.get(host)
        access_token = response.json().get("access_token")
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/add"
        with open(url, 'rb') as f:
            image = base64.b64encode(f.read())
        body = {
            "image": image,
            "image_type": "BASE64",
            "group_id": "N1",
            "user_id": userId,
            "quality_control": "NONE",
            "liveness_control": "NONE",
        }

        headers = {"Content-Type": "application/json"}
        request_url = f"{request_url}?access_token={access_token}"
        response = requests.post(request_url, headers=headers, data=body)
        result = json.loads(response.content.decode("UTF-8"))
        if result['result'] == None:
            return "未检测到人脸"
        else:
            count_sql = "SELECT COUNT(*) AS num FROM userAndphoto WHERE userId = '" + userId + "'"
            cursor.execute(count_sql)
            num = cursor.fetchall()
            cursor.execute(ver_sql)
            if num[0][0] > 0:
                QMessageBox.information(self, "提示", "您已经在系统中了，继续录入人脸将提高识别准确度！", QMessageBox.Yes)
            else:
                sql = "INSERT INTO userAndphoto(userId,name,pc) VALUES ('%s','%s',%d)" % (userId, name, 0)
                try:
                    cursor.execute(sql)
                    db.commit()
                except Exception as e:
                    print(e)
                    db.rollback()
            db.close()
