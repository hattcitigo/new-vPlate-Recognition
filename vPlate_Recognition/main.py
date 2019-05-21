from flask import Flask, render_template, request, jsonify
from datetime import datetime
from werkzeug.utils import secure_filename
from detect import detect
import os
from keras import backend as K
import logging
from datetime import datetime
import config
from yolo import YOLO
import constant

app = Flask(__name__)

UPLOAD_FOLDER = config.UPLOAD_FOLDER
if not os.path.isdir(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

log_web = logging.getLogger('Logging_Web')

# create the handler for the main logger
file_logger = logging.FileHandler('log/Licence_Plate_Recognition_Web.log')
NEW_FORMAT = '[%(asctime)s] - [%(levelname)s] - %(message)s'
file_logger_format = logging.Formatter(NEW_FORMAT)

# tell the handler to use the above format
file_logger.setFormatter(file_logger_format)

# finally, add the handler to the base logger
log_web.addHandler(file_logger)

# remember that by default, logging will start at 'warning' unless
# we set it manually
log_web.setLevel(logging.DEBUG)


console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
logging.getLogger('Logging_Web').addHandler(console)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    try:
        file_upload = request.files['file']
        s_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S_")
        name_file_up = secure_filename(s_time + file_upload.filename)
        url_file = os.path.join(UPLOAD_FOLDER, name_file_up)
        log_web.info(constant.SAVE_IMAGE_UPLOAD + url_file)
        file_upload.save(url_file)
        result = {"status": "success", "type": "upload",
                  "name_file_up": name_file_up}
        return jsonify(result)
    except:
        result = {"status": "fail", "type": "upload"}
        return jsonify(result)


@app.route('/predict/<name_file_up>', methods=['GET'])
def predict(name_file_up):
    try:
        K.clear_session()
        url_file = os.path.join(UPLOAD_FOLDER, name_file_up)
        yolo = YOLO()
        log_web.info(constant.CALL_DETECT_WITH_IMAGE_UPLOAD + url_file)
        path_result=detect(yolo, url_file)
        K.clear_session()
        result = jsonify({"status": "success", "url_file": path_result})
        return result
    except:
       result = jsonify({"status": "fail", "url_file": url_file,
                         "type": "predict"})
       return result


if __name__ == '__main__':
    app.run(debug=True)
