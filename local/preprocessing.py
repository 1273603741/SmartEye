import cv2
from PIL import Image
import os
import subprocess
import numpy as np
from matplotlib import image as matimg
from tools.read_config import read_config


class PreProcessing:
    """
    inputing video frames or directly a video, transfer in resolution, qp etc.
    """
    def pre_process_image(self, frame, **msg_dict):
        """
        according to the image_size stored in message responsed by the server,
        local adjusts the image size of image which will be sent to the server

        :param msg_dict: image size, support 100×100 poxels， 500x500 pixels
        :param input_file: images which needs to be adjust
        :return: file save path
        """
        assert frame is not None
        image = Image.fromarray(frame)
        result_image = image.resize(tuple(msg_dict['image_size']), Image.ANTIALIAS)
        frame = np.asarray(image)
        return frame

    def pre_process_by_qp(self, frame, qp):
        """
        change the image quality
        :param frame: image frame, ndarray
        :param qp: the quality number which image changes to
        :return: image frame, ndarray
        """
        assert frame is not None
        assert qp is not None
        image = Image.fromarray(frame)
        temporary_store = read_config("store-folder", "temporary_store")
        file_path = os.path.join(temporary_store, 'temporary.jpg')
        image.save(file_path, quality=qp)
        img = Image.open(file_path)
        frame = np.array(img)
        return frame


    def pre_process_video(self, input_file, **b_r_dict):
        """
        adjust the input_file's resolution and bitrate according to the parameter b_r_tuple
        :param input_file: video file path
        :param b_r_dict: the max b_r_tuple value of video transfered to
        :return: file save path
        """
        folder_path = os.path.dirname(input_file)
        file_pre_name = os.path.basename(input_file).split(".")[0]
        file_suffix = os.path.basename(input_file).split(".")[1]
        file_path = (folder_path + "/" + file_pre_name + "_" + b_r_dict['bitrate']
                     + "_" + b_r_dict['resolution'] + "." + file_suffix)
        cmd = ("ffmpeg -i " + input_file + " -vf scale=" + b_r_dict['resolution']
               + " -b:v " + b_r_dict['bitrate'] + " -maxrate " + b_r_dict['bitrate']
               + " -bufsize 2M " + file_path)

        subprocess.Popen(cmd)
        return file_path

    # def video_bitrate_adjust(input_file, bitrate):
    #     """
    #     adjust the input_file's bitrate according to the parameter bitrate
    #
    #     :param input_file: video file path
    #     :param bitrate: the bitrate value of video transfered to
    #     :return:
    #     """
    #
    #     # function should get the original bitrate of input_file
    #     # and then transfer to the target bitrate
    #     # of course, the bitrate value should belong to a bitrate list
    #
    #
    #     result = input_file
    #     cmd = ("ffmpeg -i " + input_file + " -b:v " + bitrate +
    #            " -maxrate 2M " + " -bufsize 2M " + result)
    #     os.system(cmd)

    # def get_info(input_file, get_info):
    #
    #     json_file_name = os.path.basename(input_file).split(".")[0]
    #     video_info_cmd = ("ffprobe -i " + input_file + " -v quiet -print_format json -show_streams -select_streams v:0 > "
    #                       + json_file_name + ".json")
    #     os.system(video_info_cmd)
    #
    #     with open(json_file_name + ".json", 'r') as f:
    #         info = json.load(f)
    #         origin_bitrate = info["streams"][0]["bit_rate"]
    #         origin_resolution = str(info["streams"][0]["width"]) + ":" + str(info["streams"][0]["height"])
    #
    #     if get_info == "bitrate":
    #         return origin_bitrate
    #     else:
    #         return origin_resolution


if __name__ == '__main__':

    # image_size_adjust((500, 500), './gile1.jpg')
    pass