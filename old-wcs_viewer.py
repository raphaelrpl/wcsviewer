# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wcs_viewer_dialog_base.ui'
#
# Created: Wed May 27 13:55:47 2015
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_WCSViewerDialogBase(object):
    def setupUi(self, WCSViewerDialogBase):
        WCSViewerDialogBase.setObjectName(_fromUtf8("WCSViewerDialogBase"))
        WCSViewerDialogBase.resize(400, 300)
        self.button_box = QtGui.QDialogButtonBox(WCSViewerDialogBase)
        self.button_box.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.button_box.setObjectName(_fromUtf8("button_box"))

        self.retranslateUi(WCSViewerDialogBase)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("accepted()")), WCSViewerDialogBase.accept)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("rejected()")), WCSViewerDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(WCSViewerDialogBase)

    def retranslateUi(self, WCSViewerDialogBase):
        WCSViewerDialogBase.setWindowTitle(QtGui.QApplication.translate("WCSViewerDialogBase", "WCSViewer", None, QtGui.QApplication.UnicodeUTF8))

