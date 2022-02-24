import sys
import SystemUi as system
import AddUser as add
from PyQt5.QtWidgets import QApplication, QMainWindow

# ui1:主页面 ui2:添加用户界面
app = QApplication(sys.argv)
mainWindow1 = QMainWindow()
mainWindow2 = QMainWindow()
ui1 = system.Ui_MainWindow()
ui1.setupUi(mainWindow1)
ui2 = add.Ui_MainWindow()
ui2.setupUi(mainWindow2)
ui1.actionButton_2.clicked.connect(lambda: {mainWindow1.close(), mainWindow2.show()})
ui2.pushButton_2.clicked.connect(
    lambda: {mainWindow1.show(), ui2.lineEdit.clear(), ui2.lineEdit_2.clear(), mainWindow2.close()})
mainWindow1.show()

sys.exit(app.exec_())
