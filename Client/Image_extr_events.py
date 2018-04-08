import uuid
import os
import sys
import json
import ntpath
from Image_extr_ui import Ui_Image_Extraction
from create_api import extract_images, get_devices, fetch_timestamps
from collection_events import collectionEvents, store_coll_data
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QDialog
from PyQt4.QtCore import QCoreApplication
from PyQt4.QtGui import QMessageBox
import logging

unique_filename = str(uuid.uuid4())
stored_json = r"C:\Users\shvikram\Desktop\Sumit\json"
json_filename = os.path.join(stored_json,unique_filename+".json")

user_entry = dict()
new_rec = {}


class ImageExtractionEvents(QDialog, Ui_Image_Extraction):
    def __init__(self, parent):

        super(QDialog, self).__init__(parent)
        self.zparent = parent
        self.setup_ui()
        self.channel_lst = []

    def setup_ui(self):

        super(ImageExtractionEvents, self).setupUi(self)
        QCoreApplication.processEvents()
        # self.machine_radio.toggled.connect(self.call_ui)
        self.others_radio.toggled.connect(self.call_ui)
        self.recfile_radio.toggled.connect(self.call_timestamp_device)
        self.colln_radio.toggled.connect(self.call_ui_colln)
        self.prj_radio.toggled.connect(self.call_ui_prj)
        self.browse_recfile.clicked.connect(self.browse_file)
        self.extract_btn.clicked.connect(self.extract_images)


    def browse_file(self):
        """
        File dialog for browsing & selecting the recording files
        :return: filepath of the selected file
        """
        global new_rec

        logging.basicConfig(filename='myapp.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        logging.info('Started')


        if self.browse_recfile.text() == 'Add more files':
            ts_val = self.validate_timestamp()
            if ts_val:
                self.update_json()
            else:
                QMessageBox.warning(self, "Warning",
                                    "Missing device/channel information or Incorrect timestamp")
                return

        file_path = QtGui.QFileDialog.getOpenFileName(self, 'Choose recording file..', '.',
                                                      "Rec Files (*.rec *.rrec)")
        if file_path:
            self.rec_path.setText(file_path)
            self.browse_recfile.setText("Add more files")

            self.colln_radio.setDisabled(True)
            self.prj_radio.setDisabled(True)

        # self.list_all_formats()
        self.add_file()
        new_rec = {}
        file_path = str(self.rec_path.text())

        new_rec['path'] = file_path


    def update_json(self):
        global new_rec
        file_path = str(self.rec_path.text())

        self.select_color()

        user_entry[os.path.basename(file_path)] = new_rec
        new_rec = {}
        if not os.path.isfile(json_filename):
            with open(json_filename, mode='w') as f:
                f.write(json.dumps(user_entry, indent=2))
                f.close()
        else:
            with open(json_filename) as f:
                feeds = json.load(f)
                f.close()

            feeds.update(user_entry)
            with open(json_filename, mode='w') as f:
                f.write(json.dumps(feeds, indent=2))
                f.close()
        self.start_ts.clear()
        self.end_ts.clear()
        self.step_ts.clear()

    def add_file(self):
        """
        Adding one or more selected recordings to the json file.
        :return: json file with all selected file details
        """
        # Replace forward slashes with backward slashes
        global new_rec
        path_fslash = str(self.rec_path.text())
        file_path = ntpath.normpath(path_fslash)
        self.list_all_devices(file_path)
        self.list_timestamps(file_path)
        self.collection_path.clear()
        self.prj_path.clear()

    def call_ui(self):
        self.resize(524, 290)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 501, 271))
        self.groupBox_3.setVisible(True)

    def call_timestamp_device(self):
        if self.recfile_radio.isChecked():
            self.resize(524, 620)
            self.groupBox.setGeometry(QtCore.QRect(10, 10, 501, 600))
            self.groupBox_4.setVisible(True)
            self.groupBox_5.setVisible(True)
            self.browse_recfile.setDisabled(False)
            self.rec_path.setDisabled(False)
            self.comboBox.setDisabled(False)
            self.checkBox.setDisabled(True)
            self.start_ts.setValidator(QtGui.QDoubleValidator())
            self.end_ts.setValidator(QtGui.QDoubleValidator())
            self.step_ts.setValidator(QtGui.QDoubleValidator())

        else:
            self.browse_recfile.setDisabled(True)
            self.rec_path.setDisabled(True)
            self.browse_recfile.setText("...")
            self.rec_path.clear()

    def call_ui_prj(self):
        if self.prj_radio.isChecked():
            self.resize(524, 620)
            self.groupBox.setGeometry(QtCore.QRect(10, 10, 501, 601))
            self.groupBox_5.setVisible(True)
            self.groupBox_4.setVisible(False)
            self.browse_project.setDisabled(False)
            self.prj_path.setDisabled(False)
        else:
            self.browse_project.setDisabled(True)
            self.prj_path.setDisabled(True)

    def call_ui_colln(self):
        if self.colln_radio.isChecked():
            self.resize(524, 620)
            self.groupBox.setGeometry(QtCore.QRect(10, 10, 501, 601))
            self.groupBox_5.setVisible(True)
            self.groupBox_4.setVisible(False)
            self.collection_path.setDisabled(False)
            self.browse_bpl.setDisabled(False)
            collectionEvents(self)
        else:
            self.collection_path.setDisabled(True)
            self.browse_bpl.setDisabled(True)

    def extract_images(self):
        """
        Extract the images in a folder from the recording file(s) specified by the user
        :return: folder containing image files
        """
        if self.recfile_radio.isChecked():
            ts_val = self.validate_timestamp()

            if ts_val:
                self.update_json()
                if os.path.isfile(json_filename) and os.path.getsize(json_filename) > 0:
                    opt = extract_images(self, json_filename)
                    QMessageBox.information(self, "Note: ",
                                        "{}".format(opt))
                os.remove(json_filename)
                logging.info('Finished')
                exit()
            else:
                QMessageBox.warning(self, "Warning",
                                    "Incorrect Timestamp or Incomplete information or Incomplete channel information")
        else:
            print "Calling the collection specific methods.."
            store_coll_data(self)

        print "=========================Done========================"

    def validate_timestamp(self):
        if not self.channel_lst:

            return False

        if self.start_ts.text() or self.step_ts.text() or self.end_ts.text():

            if self.start_ts.text() and not self.end_ts.text():
                if int(self.start) <= int(self.start_ts.text()) <= int(self.end):
                    new_rec['start_time'] = str(self.start_ts.text())
                    if self.step_ts.text():
                        new_rec['step_value'] = str(self.step_ts.text())
                        return True
                    return True
                else:
                    return False

            if self.end_ts.text() and not self.start_ts.text():
                if int(self.start) <= int(self.end_ts.text()) <= int(self.end):
                    new_rec['end_time'] = str(self.end_ts.text())
                    if self.step_ts.text():
                        new_rec['step_value'] = str(self.step_ts.text())
                        return True
                    return True
                else:
                    return False

            if self.step_ts.text() and not self.end_ts.text() and not self.start_ts.text():
                new_rec['step_value'] = str(self.step_ts.text())
                return True

            if self.start_ts.text() and self.end_ts.text():
                if int(self.start) <= int(self.start_ts.text()) <= int(self.end):
                    if int(self.start) <= int(self.end_ts.text()) <= int(self.end):
                        if int(self.start_ts.text()) < int(self.end_ts.text()):
                            new_rec['start_time'] = str(self.start_ts.text())
                            new_rec['end_time'] = str(self.end_ts.text())
                            if self.step_ts.text():
                                new_rec['step_value'] = str(self.step_ts.text())
                                return True
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False

        else:
            return True


    def list_all_devices(self, rec_file):
        """
        Lists all the available devices inside the recording file
        :param rec_file:
        :return:
        """
        self.comboBox.clear()

        output = get_devices(rec_file)

        all_device_list = output.split()
        all_device_list = [x.upper() for x in all_device_list]

        base_device_list = ['CSF', 'LPOS', 'VIDEO', 'MFC', 'MFC4XX', 'SRLCAM4XX']

        supported_devices = set(all_device_list).intersection(base_device_list)

        if len(supported_devices) == 0:
            QMessageBox.warning(self, "Warning",
                                "NO DEVICE SUPPORTED FOR THIS Recording. \nPlease choose another file")
            self.rec_path.clear()
            self.browse_recfile.setText("...")
            # self.browse_file()

        else:
            supported_devices = list(supported_devices)
            supported_devices.insert(0,'(select)')

            for i in supported_devices:
                self.comboBox.addItem(i.lower())

            self.comboBox.currentIndexChanged.connect(self.list_all_channels)
            self.checkBox.setEnabled(True)

    def list_all_channels(self):
        """
        Lists all the channels corresponding to a particular device selected
        :return:
        """
        global new_rec
        if str(self.comboBox.currentText()) != "(select)":
            new_rec['device'] = str(self.comboBox.currentText())
            self.comboBox_2.setDisabled(False)

        mfc = ["MFC3xx_short_image_left", "MFC3xx_long_image_left", "MFC3xx_short_image_right", "MFC3xx_long_image_right"]
        mfc4xx = ["MFC4xx_short_image_left", "MFC4xx_long_image_left", "MFC4xx_short_image_right", "MFC4xx_long_image_right"]
        srlcam4xx = ["SRLCAM4xx_short_image", "SRLCAM4xx_long_image"]
        video = ["Video Grabber FRONT", "Video Grabber LEFT", "Video Grabber REAR", "Video Grabber RIGHT"]

        self.comboBox_2.clear()

        self.comboBox_2.addItem('(select)')

        if self.comboBox.currentText() == "mfc4xx":

            for i in range(len(mfc4xx)):
                self.comboBox_2.addItem(mfc4xx[i])
                item = self.comboBox_2.model().item(i+1, 0)
                item.setCheckState(QtCore.Qt.Unchecked)

        if self.comboBox.currentText() == "mfc":
            for i in range(len(mfc)):
                self.comboBox_2.addItem(mfc[i])
                item = self.comboBox_2.model().item(i, 0)
                item.setCheckState(QtCore.Qt.Unchecked)

        if self.comboBox.currentText() == "srlcam4xx":
            for i in range(len(srlcam4xx)):
                self.comboBox_2.addItem(srlcam4xx[i])
                item = self.comboBox_2.model().item(i, 0)
                item.setCheckState(QtCore.Qt.Unchecked)

        if self.comboBox.currentText() == "video":
            for i in range(len(video)):
                self.comboBox_2.addItem(video[i])
                item = self.comboBox_2.model().item(i, 0)
                item.setCheckState(QtCore.Qt.Unchecked)




        self.comboBox_2.activated.connect(self.list_all_formats)

    def list_all_formats(self):
        """
        Lists all the file formats that are available in extraction
        :return:
        """
        global new_rec

        model = self.comboBox_2.model()
        for row in range(model.rowCount()):
            item = model.item(row)
            if item.checkState() == QtCore.Qt.Checked:
                if str(item.text()) not in self.channel_lst:
                    self.channel_lst.append(str(item.text()))
            else:
                if str(item.text()) in self.channel_lst:
                    self.channel_lst.remove(str(item.text()))

        if str(self.comboBox_2.currentText()) != "(select)":
            new_rec['channel'] = list(set(self.channel_lst))

        self.comboBox_3.clear()
        self.comboBox_3.setDisabled(False)

        all_formats = ['jpeg', 'bmp', 'avi', 'pgm', 'png', 'pfds']
        all_formats.insert(0, '(select)')

        for i in all_formats:
            self.comboBox_3.addItem(i)

        self.comboBox_3.currentIndexChanged.connect(self.get_format)

    def get_format(self):
        global new_rec
        self.checkBox.setDisabled(False)

        if str(self.comboBox_3.currentText()) != "(select)":
            new_rec['file_format'] = str(self.comboBox_3.currentText())

        if str(self.comboBox_3.currentText()) == "avi" or str(self.comboBox_3.currentText()) == "pfds":
            self.checkBox.setDisabled(True)

    def list_timestamps(self, rec_file):
        """
        Displays the start & end timestamps of the recording file to the user
        :param rec_file:
        :return:
        """
        global new_rec

        output = fetch_timestamps(rec_file)
        b = output.split()

        if b[0] == 'StartTime:':
            temp = 'Select the timestamp between these: '
            self.start = str(b[1])
            self.end = str(b[3])
            final = temp + self.start +' and '+ self.end
            self.lbl_start_end_ts.setText(final)
        else:
            self.lbl_start_end_ts.setText("ERROR!!!Cannot fetch timestamps")

    def select_color(self):
        global new_rec
        if self.checkBox.isChecked():
            new_rec['color'] = 'RGB'


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = QtGui.QWidget()
    obj = ImageExtractionEvents(window)
    sys.exit(app.exec_())
