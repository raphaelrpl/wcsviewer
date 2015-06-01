from PyQt4 import QtGui
from PyQt4.QtGui import QTableView
from PyQt4.QtGui import QVBoxLayout
from utils import CoverageTableModel
import sys


my_array = [['00', '01'],
            ['10', '11']]


class WCSWindow(QtGui.QWidget):
    def __init__(self):
        super(WCSWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.resize(800, 600)
        self.center()
        self.setWindowTitle('Center')
        tablemodel = CoverageTableModel(my_array, self)
        self.tableview = QTableView()
        self.tableview.setModel(tablemodel)
        layout = QVBoxLayout(self)
        layout.addWidget(self.tableview)
        self.setLayout(layout)
        self.show()
        self.tableview.doubleClicked.connect(self.coverageDoubleClick)

    def coverageDoubleClick(self, mi):
        row = mi.row()
        col = mi.column()
        print(row, col)

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ex = WCSWindow()
    sys.exit(app.exec_())