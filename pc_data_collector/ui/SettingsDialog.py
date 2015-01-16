# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/SettingsDialog.ui'
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

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        SettingsDialog.setObjectName(_fromUtf8("SettingsDialog"))
        SettingsDialog.resize(422, 329)
        self.gridLayout_2 = QtGui.QGridLayout(SettingsDialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_8 = QtGui.QLabel(SettingsDialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 8, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 10, 0, 1, 1)
        self.label = QtGui.QLabel(SettingsDialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(SettingsDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.cbActivateDataCollection = QtGui.QCheckBox(SettingsDialog)
        self.cbActivateDataCollection.setObjectName(_fromUtf8("cbActivateDataCollection"))
        self.gridLayout.addWidget(self.cbActivateDataCollection, 2, 1, 1, 1)
        self.label_6 = QtGui.QLabel(SettingsDialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)
        self.label_3 = QtGui.QLabel(SettingsDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.cbActivateLocalStorage = QtGui.QCheckBox(SettingsDialog)
        self.cbActivateLocalStorage.setObjectName(_fromUtf8("cbActivateLocalStorage"))
        self.gridLayout.addWidget(self.cbActivateLocalStorage, 3, 1, 1, 1)
        self.label_4 = QtGui.QLabel(SettingsDialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.label_7 = QtGui.QLabel(SettingsDialog)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 7, 0, 1, 1)
        self.lPlugwiseHost = QtGui.QLineEdit(SettingsDialog)
        self.lPlugwiseHost.setObjectName(_fromUtf8("lPlugwiseHost"))
        self.gridLayout.addWidget(self.lPlugwiseHost, 7, 1, 1, 1)
        self.label_9 = QtGui.QLabel(SettingsDialog)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 9, 0, 1, 1)
        self.lUpstreamHost = QtGui.QLineEdit(SettingsDialog)
        self.lUpstreamHost.setObjectName(_fromUtf8("lUpstreamHost"))
        self.gridLayout.addWidget(self.lUpstreamHost, 9, 1, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.btSave = QtGui.QPushButton(SettingsDialog)
        self.btSave.setObjectName(_fromUtf8("btSave"))
        self.horizontalLayout.addWidget(self.btSave)
        self.btCancel = QtGui.QPushButton(SettingsDialog)
        self.btCancel.setObjectName(_fromUtf8("btCancel"))
        self.horizontalLayout.addWidget(self.btCancel)
        self.gridLayout.addLayout(self.horizontalLayout, 11, 1, 1, 1)
        self.label_5 = QtGui.QLabel(SettingsDialog)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 6, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 7, 2, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lLocalStorage = QtGui.QLabel(SettingsDialog)
        self.lLocalStorage.setMinimumSize(QtCore.QSize(150, 0))
        self.lLocalStorage.setObjectName(_fromUtf8("lLocalStorage"))
        self.horizontalLayout_2.addWidget(self.lLocalStorage)
        self.btSelectPath = QtGui.QPushButton(SettingsDialog)
        self.btSelectPath.setObjectName(_fromUtf8("btSelectPath"))
        self.horizontalLayout_2.addWidget(self.btSelectPath)
        self.gridLayout.addLayout(self.horizontalLayout_2, 4, 1, 1, 1)
        self.lMacAddress = QtGui.QLineEdit(SettingsDialog)
        self.lMacAddress.setObjectName(_fromUtf8("lMacAddress"))
        self.gridLayout.addWidget(self.lMacAddress, 6, 1, 1, 1)
        self.label_10 = QtGui.QLabel(SettingsDialog)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout.addWidget(self.label_10, 1, 0, 1, 1)
        self.lComputerName = QtGui.QLineEdit(SettingsDialog)
        self.lComputerName.setObjectName(_fromUtf8("lComputerName"))
        self.gridLayout.addWidget(self.lComputerName, 1, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)

        self.retranslateUi(SettingsDialog)
        QtCore.QMetaObject.connectSlotsByName(SettingsDialog)

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(_translate("SettingsDialog", "Dialog", None))
        self.label_8.setText(_translate("SettingsDialog", "Upload", None))
        self.label.setText(_translate("SettingsDialog", "Datensammlung", None))
        self.label_2.setText(_translate("SettingsDialog", "Datensammlung", None))
        self.cbActivateDataCollection.setText(_translate("SettingsDialog", "Aktivieren", None))
        self.label_6.setText(_translate("SettingsDialog", "Plugwise", None))
        self.label_3.setText(_translate("SettingsDialog", "Lokale Speicherung", None))
        self.cbActivateLocalStorage.setText(_translate("SettingsDialog", "Aktivieren", None))
        self.label_4.setText(_translate("SettingsDialog", "Speicherort", None))
        self.label_7.setText(_translate("SettingsDialog", "Host", None))
        self.label_9.setText(_translate("SettingsDialog", "Host", None))
        self.btSave.setText(_translate("SettingsDialog", "Speichern", None))
        self.btCancel.setText(_translate("SettingsDialog", "Abbrechen", None))
        self.label_5.setText(_translate("SettingsDialog", "MAC-Addresse", None))
        self.lLocalStorage.setText(_translate("SettingsDialog", "TextLabel", None))
        self.btSelectPath.setText(_translate("SettingsDialog", "...", None))
        self.label_10.setText(_translate("SettingsDialog", "Computername", None))

