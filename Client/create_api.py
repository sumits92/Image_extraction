import yaml
import requests
from json import loads
from PyQt4.QtGui import QMessageBox

MAIN_URL = r"http://127.0.0.1:5000"

QRY_OUTPUT = 'qry_output'

# exec_file = r"C:\Users\uidk5887\Desktop\NewImage Extractor\61_Bin\RecFileExtractor.exe"
# output_folder = r'C:\Users\uidk5887\Desktop\Images'
# shared_loc = r'C:\Users\uidk5887\Desktop\shared_folder'

output_folder = r'C:\Users\shvikram\Desktop\Sumit\Images'
shared_loc = r'C:\Users\shvikram\Desktop\Sumit\shared_folder'

success = 0
fail = 0

def extract_images(self, json_filename):
    if json_filename:
        with open(json_filename, 'r') as f:
            json_data = yaml.safe_load(f)

    for dict_item in json_data.iteritems():
        input_parameters = dict()
        input_parameters['rec_name'] = dict_item[0]
        temp_dict = dict_item[1]

        print "dict_item is ", dict_item
        try:
            for item in dict_item[1]['channel']:
                temp_dict['channel'] = item

                input_parameters.update(dict_item[1])
                print "input parameters", input_parameters
                response_data = requests.get(url=MAIN_URL + '/extract_images',
                                             params=input_parameters)
                output = loads(response_data.text)

            try:
                global success
                global fail

                output_temp = output.split()
                if output_temp[2] == 'successfully':
                    success = success+1
                else:
                    fail = fail+1

                print 'success', success
                print 'fail', fail
                print output
            except:
                pass

        except:
            print "Error in device/channel info"
            QMessageBox.warning(self, "Warning", "Invalid selection of recording files/parameters.")
            exit()

    # os.remove(stored_json)

        try:
            import shutil, os
            shutil.rmtree(output_folder)
            os.mkdir(output_folder)

            for item in os.listdir(shared_loc):
                if item.endswith(".zip"):
                    os.remove(shared_loc + '\\' + str(item))
        except:
            pass

    return output


def get_devices(rec_file):
    input_parameters = dict()
    input_parameters['path'] = rec_file
    response_data = requests.get(url=MAIN_URL + '/get_devices',
                                 params=input_parameters)
    output = yaml.safe_load(response_data.text)
    return output


def fetch_timestamps(rec_file):
    input_parameters = dict()
    input_parameters['path'] = rec_file

    response_data = requests.get(url=MAIN_URL + '/fetch_timestamps',
                                 params=input_parameters)
    output = yaml.safe_load(response_data.text)
    return output
