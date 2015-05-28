from PyQt4.QtCore import QAbstractTableModel, QVariant, Qt


class CoverageTableModel(QAbstractTableModel):
    header_labels = ['Column 1', 'Column 2', 'Column 3', 'Column 4']

    def __init__(self, datain, parent=None, *args):
        QAbstractTableModel.__init__(self, parent)
        self.arraydata = datain

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.header_labels[section]
        return QAbstractTableModel.headerData(self, section, orientation, role)

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self.arraydata)

    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self.arraydata[0])

    def data(self, QModelIndex, int_role=None):
        if not QModelIndex.isValid():
            return QVariant()
        elif int_role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.arraydata[QModelIndex.row()][QModelIndex.column()])