import os
import json
import re
import uuid
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QDialog
from PyQt4.QtCore import QCoreApplication
from PyQt4.QtGui import QMessageBox
from Image_extr_ui import Ui_Image_Extraction
from create_api import extract_images, success, fail

json_dict = {}

unique_filename = str(uuid.uuid4())
stored_json = r"C:\Users\shvikram\Desktop\Sumit\json"
json_filename = os.path.join(stored_json,unique_filename+".json")


class collectionEvents(QDialog, Ui_Image_Extraction):

    def __init__(self, parent):
        super(QDialog, self).__init__(parent)
        self.zparent = parent
        self.setup_ui()
        self.channel_lst = []

    def setup_ui(self):
        self.zparent.comboBox_2.setDisabled(True)
        self.zparent.extract_btn.setDisabled(True)
        QCoreApplication.processEvents()
        self.zparent.browse_bpl.clicked.connect(self.browse_bpl_file)
        self.zparent.comboBox_3.currentIndexChanged.connect(self.select_bpl_formats)
        self.zparent.checkBox.stateChanged.connect(self.select_bpl_color)

    def browse_bpl_file(self):
        bpl_path = QtGui.QFileDialog.getOpenFileName(self, 'Choose BPL file..', '.',
                                                      "BPL Files (*.bpl)")
        if bpl_path:
            self.zparent.collection_path.setText(bpl_path)
            self.read_bpl(bpl_path)

    def read_bpl(self, bpl_path):
        self.rec_lst = []

        with open(bpl_path) as fname:
            start = '<BatchEntry fileName="'
            end = '">'
            for line in fname.readlines():
                if "fileName" in line:
                    result = re.search('%s(.*)%s' % (start, end), line).group(1)
                    self.rec_lst.append(result)

        for file in self.rec_lst:
            rec_dict = {}
            rec_dict['path'] = file
            json_dict[os.path.basename(file)] = rec_dict

        self.zparent.recfile_radio.setDisabled(True)
        self.zparent.prj_radio.setDisabled(True)
        self.list_devices()

    def list_devices(self):
        base_device_list = ['(select)','CSF', 'LPOS', 'VIDEO', 'MFC', 'MFC4XX', 'SRLCAM4XX']

        for i in base_device_list:
            self.zparent.comboBox.addItem(i.lower())
        self.zparent.comboBox.currentIndexChanged.connect(self.list_all_channels)

    def list_all_channels(self):
        """
        Lists all the channels corresponding to a particular device selected
        :return:
        """
        global new_rec

        self.zparent.checkBox.setEnabled(True)
        for item in json_dict.values():
            if str(self.zparent.comboBox.currentText()) != "(select)":
                item['device'] = str(self.zparent.comboBox.currentText())
                self.zparent.comboBox_2.setDisabled(False)

        mfc = ["MFC3xx_short_image_left", "MFC3xx_long_image_left", "MFC3xx_short_image_right", "MFC3xx_long_image_right"]
        mfc4xx = ["MFC4xx_short_image_left", "MFC4xx_long_image_left", "MFC4xx_short_image_right", "MFC4xx_long_image_right"]
        srlcam4xx = ["SRLCAM4xx_short_image", "SRLCAM4xx_long_image"]
        video = ["Video Grabber FRONT", "Video Grabber LEFT", "Video Grabber REAR", "Video Grabber RIGHT"]

        self.zparent.comboBox_2.clear()
        self.zparent.comboBox_2.addItem('(select)')

        if self.zparent.comboBox.currentText() == "mfc4xx":
            for i in range(len(mfc4xx)):
                self.zparent.comboBox_2.addItem(mfc4xx[i])
                item = self.zparent.comboBox_2.model().item(i+1, 0)
                item.setCheckState(QtCore.Qt.Unchecked)

        if self.zparent.comboBox.currentText() == "mfc":
            for i in range(len(mfc)):
                self.zparent.comboBox_2.addItem(mfc[i])
                item = self.zparent.comboBox_2.model().item(i+1, 0)
                item.setCheckState(QtCore.Qt.Unchecked)

        if self.zparent.comboBox.currentText() == "srlcam4xx":
            for i in range(len(srlcam4xx)):
                self.zparent.comboBox_2.addItem(srlcam4xx[i])
                item = self.zparent.comboBox_2.model().item(i+1, 0)
                item.setCheckState(QtCore.Qt.Unchecked)

        if self.zparent.comboBox.currentText() == "video":
            for i in range(len(video)):
                self.zparent.comboBox_2.addItem(video[i])
                item = self.zparent.comboBox_2.model().item(i+1, 0)
                item.setCheckState(QtCore.Qt.Unchecked)

        self.zparent.comboBox_2.activated.connect(self.list_bpl_formats)

    def list_bpl_formats(self):
        global new_rec

        model = self.zparent.comboBox_2.model()
        for row in range(model.rowCount()):
            item = model.item(row)
            if item.checkState() == QtCore.Qt.Checked:
                if str(item.text()) not in self.channel_lst:
                    self.channel_lst.append(str(item.text()))
            else:
                if str(item.text()) in self.channel_lst:
                    self.channel_lst.remove(str(item.text()))

        self.zparent.extract_btn.setDisabled(False)
        self.zparent.comboBox_3.clear()
        self.zparent.comboBox_3.setDisabled(False)

        for item in json_dict.values():
            if str(self.zparent.comboBox_2.currentText()) != "(select)":
                item['channel'] = list(set(self.channel_lst))

        all_formats = ['jpeg', 'bmp', 'avi', 'pgm', 'png', 'pfds']
        all_formats.insert(0, '(select)')

        for i in all_formats:
            self.zparent.comboBox_3.addItem(i)
        self.select_bpl_formats()

    def select_bpl_formats(self):
        self.zparent.checkBox.setDisabled(False)

        for item in json_dict.values():
            item['file_format'] = str(self.zparent.comboBox_3.currentText())

        self.update_json_colln()

        if str(self.zparent.comboBox_3.currentText()) == "avi" or str(self.zparent.comboBox_3.currentText()) == "pfds":
            self.zparent.checkBox.setDisabled(True)

    def select_bpl_color(self):
        if self.zparent.checkBox.isChecked():
            for item in json_dict.values():
                item['color'] = 'RGB'

        else:
            for item in json_dict.values():
                item['color'] = '(select)'

        self.update_json_colln()

    def update_json_colln(self):
        if not os.path.isfile(json_filename):
            with open(json_filename, mode='w') as f:
                f.write(json.dumps(json_dict, indent=2))
                f.close()
        else:
            with open(json_filename) as f:
                feeds = json.load(f)
                f.close()

            feeds.update(json_dict)
            with open(json_filename, mode='w') as f:
                f.write(json.dumps(feeds, indent=2))
                f.close()


def store_coll_data(self):
    opt = extract_images(self, json_filename)
    from create_api import success, fail

    QMessageBox.information(self, "Note: ",
                            "Successfully extracted recordings: {} \n"
                            "Failed/Discarded recordings : {} \n".format(success, fail))
    os.remove(json_filename)
    exit()
