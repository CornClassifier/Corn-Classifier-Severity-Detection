from flask import Flask, render_template, request
import cv2
import numpy as np
from PIL import Image
import skimage
from skimage import transform
from scipy import ndimage
from skimage.color import rgb2gray
from predict import *


app = Flask(__name__)

toReturn = ['']
severityReturn = ['']
default_img = './static/images/upload-img.jpg'

model = init_model()


@app.route('/', methods=['GET', 'POST'])
def home_page():
    toReturn = [default_img]
    severityReturn = [default_img]
    return render_template('index.html', data=toReturn, severe=severityReturn, tab="classify")


@app.route('/classify', methods=['POST'])
def classify():
    imgFile = request.files['imgFile']
    image_path = './static/images/uploaded/' + imgFile.filename
    imgFile.save(image_path)

    result = predict(model, image_path)

    toReturn = [image_path, result]
    severityReturn = [default_img]

    print(image_path)
    print(toReturn)

    return render_template('index.html', data=toReturn, severe=severityReturn, tab="classify")


@app.route('/severity', methods=['POST'])
def severity():
    imgFile = request.files['severityFile']
    image_path = './static/images/uploaded/' + imgFile.filename
    imgFile.save(image_path)
    Img_size = 256

    if type(image_path) == str:
        img_array = cv2.imread(image_path, cv2.IMREAD_COLOR)
        new_img = cv2.resize(img_array, (Img_size, Img_size))
        gray = rgb2gray(new_img)
    else:
        gray = rgb2gray(image_path)
    gray_r = gray.reshape(gray.shape[0]*gray.shape[1])
    for i in range(gray_r.shape[0]):
        if gray_r[i] > gray_r.mean():
            gray_r[i] = 256
        elif gray_r[i] > 0.5:
            gray_r[i] = 256
        elif gray_r[i] > 0.25:
            gray_r[i] = 0
        else:
            gray_r[i] = 0
    gray = gray_r.reshape(gray.shape[0], gray.shape[1])
    x1 = 0
    gr = gray.reshape(-1)
    for i in range(gray.shape[0]*gray.shape[1]):
        if gr[i] != 0:
            x1 += 1
    y1 = gray.shape[0]*gray.shape[1]
    z = (y1-x1)/y1
    print("Percent of infected part is ", z*100, "%")
    percentage_num = z*100
    if z < 0.25:
        print("Severity rating is 1 ")
        print("Slight Infection")

        severityReturn = [image_path, str(percentage_num) + '%',
                          "1", "Slight Infection"]
    elif z < 0.50 and z >= 0.25:
        print("Severity rating is 2 ")
        print("Moderate Infection")

        severityReturn = [image_path, str(percentage_num) + '%',
                          "2", "Moderate Infection"]

    else:
        print("Severity rating is 3 ")
        print("Very Heavy Infection")
        severityReturn = [image_path, str(percentage_num) + '%',
                          "3", "Very Heavy Infection"]

    toReturn = [default_img]

    return render_template('index.html', severe=severityReturn, data=toReturn, tab="severe")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
