from keras.models import load_model
from PIL import Image, ImageOps, ImageFont, ImageDraw
import numpy as np
from keras import backend as K
import pandas as pd
from sklearn.preprocessing import LabelEncoder


def predict_JP(path_image, crop):
    folder_ex = 'model_data/train.json'
    arr_label = np.array(pd.read_json(folder_ex)['Line'])

    H = []
    for i in arr_label:
        H += i
    elements = np.unique(H)

    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(elements)

    img_w = 160
    img_h = 110

    model1 = load_model('model_data/Model_ver1')
    
    def process_0_each_data(img):
        #img = Image.open(path)
        img = img.resize((160, 110))
        img = img.convert("L")
        img = ImageOps.invert(img)
        ar_img = np.array(img)
        ar_img[ar_img > 40] = 255
        ar_img[ar_img <= 40] = 0
        ar_img = ar_img/255
        return ar_img

    def to_input(data_set):
        X_new11 = []
        for i in range(len(data_set)):
            X_new11.append(data_set[i].T)

        X_new12 = []
        for i in range(len(X_new11)):
            a = np.transpose(X_new11[i][np.newaxis], (1, 2, 0))
            X_new12.append(a)

        X_new12 = np.array(X_new12)
        return X_new12

    def decode(test):
        a, b = K.ctc_decode(
            y_pred=model1.predict(test),
            input_length=[(img_w//2)//2//2]*len(test),
            greedy=True,
            beam_width=200,
            top_paths=1)
        return K.get_value(a[0])

    def decode_num(encode_list):
        decode_list = []
        for i in range(len(encode_list)):
            decode_row = []
            for j in range(len(encode_list[i])):
                for k in range(len(integer_encoded)):
                    if encode_list[i][j] == integer_encoded[k]:
                        decode_row.append(elements[k])
            decode_list.append(decode_row)
        return decode_list
        
    img_return = path_image

    font = ImageFont.truetype(font='font/FiraMono-Medium.otf',
                                size=np.floor(3e-2 * img_return.size[1] + 15).astype('int32'))
    thickness = (img_return.size[0] + img_return.size[1]) // 300

    for i in crop: 
        left = i[0]
        top = i[1]
        right = i[2]
        bottom = i[3]
        img = img_return.crop(i)
        arr = process_0_each_data(img)
        arr1 = to_input([arr])
        t = decode(arr1)
        t = decode_num(t)[0]
        t = "".join(i for i in t)
        draw = ImageDraw.Draw(img_return)
        label = '{}'.format(t)
        label_size = draw.textsize(label, font)
        if top - label_size[1] >= 0:
            text_origin = np.array([left, top - label_size[1]])
        else:
            text_origin = np.array([left, top + 1])

        # My kingdom for a good redistributable image drawing library.
        for i in range(thickness):
            draw.rectangle([left + i, top + i, right - i, bottom - i], outline='red')
        draw.rectangle([tuple(text_origin), tuple(text_origin + label_size)], fill='red')
        draw.text(text_origin, label, fill=(0, 0, 0), font=font)
        del draw
    return img_return
