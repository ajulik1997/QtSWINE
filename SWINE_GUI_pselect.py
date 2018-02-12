# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\ISIS STFC\Desktop\SWINE_GUI\SWINE_GUI_pselect.ui'
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
        Dialog.resize(270, 160)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(270, 160))
        Dialog.setMaximumSize(QtCore.QSize(270, 160))
        font = QtGui.QFont()
        font.setPointSize(12)
        Dialog.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("../../.designer/backup/icon.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setModal(True)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 110, 231, 41))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayoutWidget = QtGui.QWidget(Dialog)
        self.formLayoutWidget.setEnabled(True)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 251, 95))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignCenter)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignCenter)
        self.formLayout.setMargin(5)
        self.formLayout.setSpacing(5)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.lbl_s1p = QtGui.QLabel(self.formLayoutWidget)
        self.lbl_s1p.setEnabled(True)
        self.lbl_s1p.setObjectName(_fromUtf8("lbl_s1p"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.lbl_s1p)
        self.lbl_s2p = QtGui.QLabel(self.formLayoutWidget)
        self.lbl_s2p.setEnabled(True)
        self.lbl_s2p.setObjectName(_fromUtf8("lbl_s2p"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.lbl_s2p)
        self.lbl_samp = QtGui.QLabel(self.formLayoutWidget)
        self.lbl_samp.setEnabled(True)
        self.lbl_samp.setObjectName(_fromUtf8("lbl_samp"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.lbl_samp)
        self.spb_s1p = QtGui.QDoubleSpinBox(self.formLayoutWidget)
        self.spb_s1p.setCorrectionMode(QtGui.QAbstractSpinBox.CorrectToNearestValue)
        self.spb_s1p.setSingleStep(0.01)
        self.spb_s1p.setObjectName(_fromUtf8("spb_s1p"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.spb_s1p)
        self.spb_s2p = QtGui.QDoubleSpinBox(self.formLayoutWidget)
        self.spb_s2p.setCorrectionMode(QtGui.QAbstractSpinBox.CorrectToNearestValue)
        self.spb_s2p.setSingleStep(0.01)
        self.spb_s2p.setObjectName(_fromUtf8("spb_s2p"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.spb_s2p)
        self.spb_samp = QtGui.QDoubleSpinBox(self.formLayoutWidget)
        self.spb_samp.setCorrectionMode(QtGui.QAbstractSpinBox.CorrectToNearestValue)
        self.spb_samp.setSingleStep(0.01)
        self.spb_samp.setObjectName(_fromUtf8("spb_samp"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.spb_samp)
        self.formLayoutWidget.raise_()
        self.buttonBox.raise_()

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Parameter position select", None))
        self.lbl_s1p.setText(_translate("Dialog", "Position of slit 1 (m):", None))
        self.lbl_s2p.setText(_translate("Dialog", "Position of slit 2 (m):", None))
        self.lbl_samp.setText(_translate("Dialog", "Position of sample (m):", None))

