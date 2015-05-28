from PyQt4 import QtGui
from PyQt4.QtGui import QTableView
from PyQt4.QtGui import QVBoxLayout
from utils import CoverageTableModel
import sys


my_array = [['00', '01', '02'],
            ['10', '11', '12'],
            ['20', '21', '22']]


class WCSWindow(QtGui.QWidget):
    def __init__(self):
        super(WCSWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.resize(800, 600)
        self.center()
        self.setWindowTitle('Center')
        tablemodel = CoverageTableModel(my_array, self)
        tableview = QTableView()
        tableview.setModel(tablemodel)
        layout = QVBoxLayout(self)
        layout.addWidget(tableview)
        self.setLayout(layout)
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ex = WCSWindow()
    sys.exit(app.exec_())