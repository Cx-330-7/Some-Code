import sys
import ManageUi as mgui
from PyQt5.QtWidgets import QApplication, QMainWindow

# ui1:主页面 ui2:添加用户界面
app = QApplication(sys.argv)
mainWindow1 = QMainWindow()
mainWindow2 = QMainWindow()
ui1 = mgui.Ui_MainWindow()
ui1.setupUi(mainWindow1, mainWindow2)
mainWindow1.show()
sys.exit(app.exec_())
