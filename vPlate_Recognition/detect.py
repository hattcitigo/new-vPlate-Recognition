from cv2 import cv2
from PIL import Image
import os
from ocr import predict_JP
from keras import backend as K
import logging
import config
import constant
FOLDER_IMAGE_CROP = os.path.join("static","crop")
FOLDER_IMAGE_RESULT = os.path.join("static","result")
from yolo import YOLO
LOGGING_NAME_FOLDER = config.LOGGING_NAME_FOLDER
if not os.path.isdir(LOGGING_NAME_FOLDER):
    os.makedirs(LOGGING_NAME_FOLDER)

##Setting logging

log = logging.getLogger('Logging_Detect')

# create the handler for the main logger
file_logger = logging.FileHandler('log/Licence_Plate_Recognition_Detect.log')
NEW_FORMAT = '[%(asctime)s] - [%(levelname)s] - %(message)s'
file_logger_format = logging.Formatter(NEW_FORMAT)

# tell the handler to use the above format
file_logger.setFormatter(file_logger_format)

# finally, add the handler to the base logger
log.addHandler(file_logger)

# remember that by default, logging will start at 'warning' unless
# we set it manually
log.setLevel(logging.DEBUG)


console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
logging.getLogger('Logging_Detect').addHandler(console)
yolo = YOLO()
def detect(path_img):
    try:
        img_in = Image.open(path_img)
        log.info(constant.RUN_YOLO_DETECT_IMAGE + path_img)
        img_out,crop = yolo.detect_image(img_in)
        image = predict_JP(img_out,crop)
        name = path_img.split("\\")[-1]
        name = name.split(".")[0]
        path_result = os.path.join(FOLDER_IMAGE_RESULT, name + '.png')
        log.info(constant.SAVE_IMAGE_LABEL_BOX + path_result)
        image.save(path_result, "PNG")
        # for i in crop:
        #     K.clear_session()
        #     #result.append([i,predict_JP(i)])
        #     log.info(constant.RUN_OCR_DETECT_IMAGE + i)
        return path_result
    except:
        log.error(constant.NO_IMAGE_OPEN + path_img)

