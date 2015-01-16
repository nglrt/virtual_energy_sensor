# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/DeviceInformation.ui'
#
# Created: Tue Jul 29 07:54:08 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_DeviceInformation(object):
    def setupUi(self, DeviceInformation):
        DeviceInformation.setObjectName(_fromUtf8("DeviceInformation"))
        DeviceInformation.resize(400, 300)
        self.verticalLayout_2 = QtGui.QVBoxLayout(DeviceInformation)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.teInfo = QtGui.QTextEdit(DeviceInformation)
        self.teInfo.setObjectName(_fromUtf8("teInfo"))
        self.verticalLayout_2.addWidget(self.teInfo)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btClose = QtGui.QPushButton(DeviceInformation)
        self.btClose.setObjectName(_fromUtf8("btClose"))
        self.horizontalLayout.addWidget(self.btClose)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(DeviceInformation)
        QtCore.QMetaObject.connectSlotsByName(DeviceInformation)

    def retranslateUi(self, DeviceInformation):
        DeviceInformation.setWindowTitle(_translate("DeviceInformation", "Form", None))
        self.btClose.setText(_translate("DeviceInformation", "Schließen", None))

