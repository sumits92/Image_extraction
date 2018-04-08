import os
import shutil
import zipfile
import ntpath
import subprocess
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flasgger import Swagger
import logging
application = Flask(__name__)

Swagger(application)
api = Api(application)

exec_file = r"C:\Users\shvikram\Desktop\Sumit\New_Rec_Extrctr\RecFileExtractor.exe"
output_folder = r'C:\Users\shvikram\Desktop\Sumit\Images'
shared_loc = r'C:\Users\shvikram\Desktop\Sumit\shared_folder'


class ExtractImages(Resource):
    """
    Get a collection ID from its name
    """
    # @authorize_access
    # @ldap.basic_auth_required
    def get(self):
        """
        Image Extraction
        ---
        tags:
            - Extracts the images
        parameters:
          - name: rec_name
            in: query
            type: string
            required: true
            description: Recording name (Continuous_2015.02.17_at_11.24.57.rec)
          - name: path
            in: query
            type: raw string
            paramType: path
            required: true
            description: Recording Path(\\\ozd0618g\\\sw\\\testHpc\\\input\\\Continuous_2015.02.17_at_11.24.57.rec)
          - name: device
            in: query
            type: string
            required: false
            nullable: true
            description: Device name for which the recording belongs.('CSF', 'LPOS', 'VIDEO', 'MFC', 'MFC4xx', 'SRLCAM4xx')
          - name: file_format
            in: query
            type: string
            nullable: true
            description: Image file format.('jpeg', 'bmp', 'avi', 'pgm','png')
          - name: channel
            in: query
            type: string
            nullable: true
            description: Channel name ("MFC3xx_short_image_left", "MFC3xx_long_image_left", "MFC3xx_short_image_right", "MFC3xx_long_image_right")
          - name: start_time
            in: query
            type: integer
            nullable: true
            description: Start timestamp from where the extraction has to start
          - name: end_time
            in: query
            type: integer
            nullable: true
            description: End timestamp till where the extraction suppose to end
        """
        parser = reqparse.RequestParser()
        parser.add_argument('rec_name', type=str)
        parser.add_argument('path', type=str)
        parser.add_argument('device', type=str)
        parser.add_argument('file_format', type=str)
        parser.add_argument('channel', type=str)
        parser.add_argument('color', type=str)
        parser.add_argument('start_time', type=str)
        parser.add_argument('end_time', type=str)
        parser.add_argument('step_value', type=str)
        args = parser.parse_args()
        self.rec_name = args['rec_name']
        self.rec_path = args['path']
        self.device = args['device']
        self.file_format = args['file_format']
        self.channel = args['channel']
        self.color = args['color']
        self.start_time = args['start_time']
        self.end_time = args['end_time']
        self.step_value = args['step_value']

        # job = hpc.Job()
        #
        # # Create the Job
        # job_folder = job.create("SHT_ALL_MFS_000000I00_RFE")
        # print(job_folder)
        #
        # # Set Project (Required!)
        # job.set_project('MFC310')
        # job_folder = "D:\\"
        # path = os.path.split(__file__)[0]
        # path = os.path.split(path)[0]
        # path = os.path.abspath(os.path.split(path)[0])
        #
        # src = os.path.join(path, r'code_without_celery\Server\new_exe\61_Bin')
        # print "Path", os.listdir(src)
        # dest = os.path.join(job_folder, r'1_Input\rfe')
        # shutil.copytree(src, dest)
        #
        # cmd = self.get_cmd()
        #
        # factory = hpc.TaskFactory(job)
        # factory.create_task(cmd)
        #
        # job.submit()

        opt = self.get_cmd()
        print "opt", opt
        if opt == -5001:
            qry_output = 'No Video Device inside *.rec File. Please select a device and re-run'
            os.rmdir(self.folder_name)
            try:
                os.rmdir(os.path.split(self.folder_name)[0])
            except:
                pass

        elif opt == 1:
            qry_output = 'Folder already exist please check'

        elif opt == 0:
            qry_output = "Images extracted successfully into {} folder".format(self.folder_name)

            # Compress the o/p in the HPC folder itself for transfer
            folder_path = os.path.split(self.folder_name)[0]
            folder_name = ntpath.basename(folder_path)
            shutil.make_archive(folder_path, 'zip', folder_path)

            # Recursively check for and delete the zip file in the shared location
            if os.path.exists(shared_loc+'\\'+folder_name+'.zip'):
                os.remove(shared_loc+'\\'+folder_name+'.zip')

            # Transfer the zip folder from HPC to shared location
            shutil.copy(folder_path + '.zip', shared_loc)

            # Create the o/p folder in the shared location for the first time
            if not os.path.exists(shared_loc + '\\' + folder_name):
                os.mkdir(shared_loc + '\\' + folder_name)

            # Unzip the files to the o/p folder in shared location
            try:
                zipp = zipfile.ZipFile(shared_loc + '\\' + folder_name + '.zip')
                zipp.extractall(shared_loc + '\\' + folder_name)
                # os.remove(shared_loc + '\\' + folder + '.zip')
            except:
                print "Error in unzipping"


        elif opt == -5013:
            qry_output = 'No MFC4xx Device inside *.rec File. Please select a different device and re-run.'
            os.rmdir(self.folder_name)
            try:
                os.rmdir(os.path.split(self.folder_name)[0])
            except:
                pass

        elif opt == -5014:
            qry_output = "No MFC4xx Image Found at Timestamp + 1 sec. Selected channel is not present for the recording."
            os.rmdir(self.folder_name)
            try:
                os.rmdir(os.path.split(self.folder_name)[0])
            except:
                pass

        elif opt == -5016:
            qry_output = "No SRLCAM4xx Device inside *.rec File. Please select a different device and re-run."
            os.rmdir(self.folder_name)
            try:
                os.rmdir(os.path.split(self.folder_name)[0])
            except:
                pass

        elif opt == -5010:
            qry_output = "No MFC3xx Device inside *.rec File. Please select a different device and re-run."
            os.rmdir(self.folder_name)
            try:
                os.rmdir(os.path.split(self.folder_name)[0])
            except:
                pass

        else:
            qry_output = 'Error in execution'

        print "qry_output >> ", qry_output
        # # db_handler.close()
        # self.remove_files()
        return qry_output

    def get_cmd(self):
        """
        Runs the .exe file to extract images for the given recording file
        :param rec_file:
        :return:
        """
        self.rec_path = ntpath.normpath(self.rec_path)
        if not self.file_format:
            self.file_format = 'jpeg'
        self.folder_name = output_folder + "\\" + os.path.splitext(self.rec_name)[0] + "_" + self.device + "\\" + self.channel + "_" + self.file_format
        if not os.path.isdir(self.folder_name):

            joined_file = exec_file + ' "' + self.rec_path + '"' + ' /O:"' + self.folder_name +'"'

            if self.start_time:
                joined_file += ' "/T:' + self.start_time + '"'

            if self.end_time:
                joined_file += ' "/U:' + self.end_time + '"'

            if self.step_value:
                joined_file += ' "/S:' + self.step_value + '"'

            if self.device:
                joined_file += ' "/D:' + self.device + '"'

            if self.channel:
                joined_file += ' "/C:' + self.channel + '"'

            if self.file_format:
                joined_file += ' "/F:' + self.file_format + '"'

            if self.color:
                joined_file += ' "/R"'

            output = subprocess.call(str(joined_file))
            # print "=========================Done========================"
            return output
        else:
            return 1


class GetDevices(Resource):
    """
    Gets the list of all supported devices for the selected recording file
    """
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('path', type=str)
        args = parser.parse_args()
        self.rec_path = args['path']
        opt = self.get_devices()
        return opt

    def get_devices(self):
        self.rec_path = ntpath.normpath(self.rec_path)
        joined_file = exec_file + ' "' + self.rec_path + '"' + ' /L:D'
        print "joined_file for get_devices --> ", joined_file
        a = subprocess.Popen(joined_file, stdout=subprocess.PIPE)
        output = a.stdout.read()
        return output


class GetTimestamps(Resource):
    """
    Fetches the start and end timestamps for the selected recording file
    """
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('path', type=str)
        args = parser.parse_args()
        self.rec_path = args['path']
        opt = self.fetch_timestamps()
        return opt

    def fetch_timestamps(self):
        self.rec_path = ntpath.normpath(self.rec_path)
        joined_file = exec_file + ' "' + self.rec_path + '"' + ' /I'
        print "joined_file for fetch_timestamps --> ", joined_file
        a = subprocess.Popen(joined_file, stdout=subprocess.PIPE)
        output = a.stdout.read()
        return output


api.add_resource(ExtractImages, '/extract_images')
api.add_resource(GetDevices, '/get_devices')
api.add_resource(GetTimestamps, '/fetch_timestamps')


if __name__ == '__main__':
    # application.run(host='10.226.226.38',port='5000')
    application.run()
