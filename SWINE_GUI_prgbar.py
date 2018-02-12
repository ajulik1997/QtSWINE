# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\ISIS STFC\Desktop\SWINE_GUI\SWINE_GUI_prgbar.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(250, 100)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(250, 100))
        Dialog.setMaximumSize(QtCore.QSize(250, 100))
        font = QtGui.QFont()
        font.setPointSize(12)
        Dialog.setFont(font)
        Dialog.setModal(True)
        self.lbl = QtGui.QLabel(Dialog)
        self.lbl.setGeometry(QtCore.QRect(10, 50, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setKerning(True)
        self.lbl.setFont(font)
        self.lbl.setFrameShape(QtGui.QFrame.NoFrame)
        self.lbl.setFrameShadow(QtGui.QFrame.Plain)
        self.lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl.setObjectName(_fromUtf8("lbl"))
        self.prg = QtGui.QProgressBar(Dialog)
        self.prg.setGeometry(QtCore.QRect(10, 10, 231, 31))
        self.prg.setProperty("value", 69)
        self.prg.setTextVisible(True)
        self.prg.setInvertedAppearance(False)
        self.prg.setObjectName(_fromUtf8("prg"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Processing...", None))
        self.lbl.setText(_translate("Dialog", "TextLabel", None))

