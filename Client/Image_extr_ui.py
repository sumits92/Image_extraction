# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Image_Extration.ui'
#
# Created: Mon Feb 26 15:43:13 2018
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!
import os,sys
from PyQt4.QtGui import QFileDialog
import json
import ntpath
import subprocess
import yaml
from PyQt4 import QtCore, QtGui




# exec_file = r"D:\Rec_Extractor\NewImage_Extractor\bin\RecFileExtractor.exe"
# output_folder = r'D:\Sample_Recs\Images'

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

class CheckableComboBox(QtGui.QComboBox):
    def __init__(self,parent):
        super(CheckableComboBox, self).__init__(parent)
        self.view().pressed.connect(self.handleItemPressed)
        self.setModel(QtGui.QStandardItemModel(self))

    def handleItemPressed(self, index):
        item = self.model().itemFromIndex(index)
        if item.checkState() == QtCore.Qt.Checked:
            item.setCheckState(QtCore.Qt.Unchecked)
        else:
            item.setCheckState(QtCore.Qt.Checked)




class Ui_Image_Extraction(object):


    def setupUi(self, Dialog):
        self.setObjectName(_fromUtf8("Dialog"))
        self.resize(524, 140)
        self.groupBox = QtGui.QGroupBox(self)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 501, 114))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.groupBox_2 = QtGui.QGroupBox(self.groupBox)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 30, 481, 71))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.machine_radio = QtGui.QRadioButton(self.groupBox_2)
        self.machine_radio.setGeometry(QtCore.QRect(10, 30, 161, 20))
        self.machine_radio.setObjectName(_fromUtf8("radioButton_3"))
        self.others_radio = QtGui.QRadioButton(self.groupBox_2)
        self.others_radio.setGeometry(QtCore.QRect(280, 30, 95, 20))
        self.others_radio.setObjectName(_fromUtf8("radioButton_4"))
        self.groupBox_3 = QtGui.QGroupBox(self.groupBox)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 110, 481, 151))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.rec_path = QtGui.QLineEdit(self.groupBox_3)
        self.rec_path.setGeometry(QtCore.QRect(120, 30, 241, 21))
        self.rec_path.setObjectName(_fromUtf8("lineEdit"))
        self.browse_recfile = QtGui.QPushButton(self.groupBox_3)
        self.browse_recfile.setGeometry(QtCore.QRect(370, 30, 100, 21))
        self.browse_recfile.setObjectName(_fromUtf8("pushButton_2"))
        self.collection_path = QtGui.QLineEdit(self.groupBox_3)
        self.collection_path.setGeometry(QtCore.QRect(120, 70, 241, 22))
        self.collection_path.setObjectName(_fromUtf8("lineEdit_2"))
        self.browse_bpl = QtGui.QPushButton(self.groupBox_3)
        self.browse_bpl.setGeometry(QtCore.QRect(370, 70, 100, 21))
        self.browse_bpl.setObjectName(_fromUtf8("pushButton_4"))
        self.prj_path = QtGui.QLineEdit(self.groupBox_3)
        self.prj_path.setGeometry(QtCore.QRect(120, 110, 241, 22))
        self.prj_path.setObjectName(_fromUtf8("lineEdit_3"))
        self.browse_project = QtGui.QPushButton(self.groupBox_3)
        self.browse_project.setGeometry(QtCore.QRect(370, 110, 100, 21))
        self.browse_project.setObjectName(_fromUtf8("pushButton_6"))
        self.recfile_radio = QtGui.QRadioButton(self.groupBox_3)
        self.recfile_radio.setGeometry(QtCore.QRect(10, 30, 95, 20))
        self.recfile_radio.setObjectName(_fromUtf8("radioButton"))
        self.colln_radio = QtGui.QRadioButton(self.groupBox_3)
        self.colln_radio.setGeometry(QtCore.QRect(10, 70, 95, 20))
        self.colln_radio.setObjectName(_fromUtf8("radioButton_2"))
        self.prj_radio = QtGui.QRadioButton(self.groupBox_3)
        self.prj_radio.setGeometry(QtCore.QRect(10, 110, 95, 20))
        self.prj_radio.setObjectName(_fromUtf8("radioButton_5"))
        self.groupBox_5 = QtGui.QGroupBox(self.groupBox)
        self.groupBox_5.setGeometry(QtCore.QRect(10, 270, 481, 141))
        self.groupBox_5.setObjectName(_fromUtf8("groupBox_5"))
        self.lbl_device = QtGui.QLabel(self.groupBox_5)
        self.lbl_device.setGeometry(QtCore.QRect(30, 30, 53, 16))
        self.lbl_device.setObjectName(_fromUtf8("label_6"))
        self.checkBox = QtGui.QCheckBox(self.groupBox_5)
        self.checkBox.setGeometry(QtCore.QRect(260, 100, 131, 31))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.comboBox_2 = CheckableComboBox(self.groupBox_5)
        self.comboBox_2.setGeometry(QtCore.QRect(260, 50, 161, 22))
        self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))
        self.lbl_color = QtGui.QLabel(self.groupBox_5)
        self.lbl_color.setGeometry(QtCore.QRect(260, 90, 53, 16))
        self.lbl_color.setObjectName(_fromUtf8("label_9"))
        self.lbl_channel = QtGui.QLabel(self.groupBox_5)
        self.lbl_channel.setGeometry(QtCore.QRect(260, 30, 53, 16))
        self.lbl_channel.setObjectName(_fromUtf8("label_7"))
        self.comboBox = QtGui.QComboBox(self.groupBox_5)
        self.comboBox.setGeometry(QtCore.QRect(30, 50, 151, 22))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox_3 = QtGui.QComboBox(self.groupBox_5)
        self.comboBox_3.setGeometry(QtCore.QRect(30, 110, 151, 22))
        self.comboBox_3.setObjectName(_fromUtf8("comboBox_3"))
        self.lbl_format = QtGui.QLabel(self.groupBox_5)
        self.lbl_format.setGeometry(QtCore.QRect(30, 90, 53, 16))
        self.lbl_format.setObjectName(_fromUtf8("label_8"))
        self.extract_btn = QtGui.QPushButton(self.groupBox)
        self.extract_btn.setGeometry(QtCore.QRect(400, 560, 93, 28))
        self.extract_btn.setObjectName(_fromUtf8("pushButton_7"))
        self.groupBox_4 = QtGui.QGroupBox(self.groupBox)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 420, 481, 131))
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.lbl_start_timestamp = QtGui.QLabel(self.groupBox_4)
        self.lbl_start_timestamp.setGeometry(QtCore.QRect(30, 60, 101, 16))
        self.lbl_start_timestamp.setObjectName(_fromUtf8("label_4"))
        self.lbl_end_timestamp = QtGui.QLabel(self.groupBox_4)
        self.lbl_end_timestamp.setGeometry(QtCore.QRect(180, 60, 91, 16))
        self.lbl_end_timestamp.setObjectName(_fromUtf8("label_5"))
        self.lbl_step_timestamp = QtGui.QLabel(self.groupBox_4)
        self.lbl_step_timestamp.setGeometry(QtCore.QRect(330, 60, 91, 20))
        self.lbl_step_timestamp.setObjectName(_fromUtf8("label_6"))
        self.start_ts = QtGui.QLineEdit(self.groupBox_4)
        self.start_ts.setGeometry(QtCore.QRect(30, 90, 113, 22))
        self.start_ts.setObjectName(_fromUtf8("lineEdit_4"))
        self.end_ts = QtGui.QLineEdit(self.groupBox_4)
        self.end_ts.setGeometry(QtCore.QRect(180, 90, 113, 22))
        self.end_ts.setObjectName(_fromUtf8("lineEdit_5"))
        self.step_ts = QtGui.QLineEdit(self.groupBox_4)
        self.step_ts.setGeometry(QtCore.QRect(330, 90, 113, 22))
        self.step_ts.setObjectName(_fromUtf8("lineEdit_6"))
        self.lbl_start_end_ts = QtGui.QLabel(self.groupBox_4)
        self.lbl_start_end_ts.setGeometry(QtCore.QRect(30, 30, 475, 16))
        self.lbl_start_end_ts.setObjectName(_fromUtf8("label"))


        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle(_translate("Dialog", "Image Extraction", None))
        self.groupBox.setTitle(_translate("Dialog", "Image Extraction", None))
        self.groupBox_2.setTitle(_translate("Dialog", "Select the purpose for Image extraction", None))
        self.machine_radio.setText(_translate("Dialog", "Machine/Deep learning", None))
        self.others_radio.setText(_translate("Dialog", "Others", None))
        self.groupBox_3.setTitle(_translate("Dialog", "Give the input", None))
        self.browse_recfile.setText(_translate("Dialog", "...", None))
        self.browse_bpl.setText(_translate("Dialog", "...", None))
        self.browse_project.setText(_translate("Dialog", "...", None))
        self.recfile_radio.setText(_translate("Dialog", "Rec File", None))
        self.colln_radio.setText(_translate("Dialog", "Collection", None))
        self.prj_radio.setText(_translate("Dialog", "Project", None))
        self.groupBox_5.setTitle(_translate("Dialog", "Give the Camera parameters", None))
        self.lbl_device.setText(_translate("Dialog", "Device", None))
        self.lbl_color.setText(_translate("Dialog", "Colour", None))
        self.lbl_channel.setText(_translate("Dialog", "Channel", None))
        self.lbl_format.setText(_translate("Dialog", "Format", None))
        self.extract_btn.setText(_translate("Dialog", "Extract", None))
        self.groupBox_4.setTitle(_translate("Dialog", "Give the timestamp", None))
        self.lbl_start_timestamp.setText(_translate("Dialog", "Start Timestamp", None))
        self.lbl_end_timestamp.setText(_translate("Dialog", "End Timestamp", None))
        self.lbl_start_end_ts.setText(_translate("Dialog", "Select the timestamp between these:", None))
        self.checkBox.setText("Extract in Color-RGB")
        self.groupBox_3.setVisible(False)
        self.groupBox_4.setVisible(False)
        self.groupBox_5.setVisible(False)
        self.rec_path.setDisabled(True)
        self.browse_recfile.setDisabled(True)
        self.browse_bpl.setDisabled(True)
        self.browse_project.setDisabled(True)
        self.prj_path.setDisabled(True)
        self.collection_path.setDisabled(True)
        self.show()






