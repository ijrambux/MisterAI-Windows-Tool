from PyQt5 import QtWidgets
from ui import MisterAITool

app = QtWidgets.QApplication([])
win = MisterAITool()
win.show()
app.exec_()
