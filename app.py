import os
import sys
import requests
import ssl
from flask import Flask, redirect, url_for, request
from flask import request
from flask import jsonify
from flask import send_file


from app_utils import download, DownloadPrecheckFailed
from app_utils import generate_random_filename
from app_utils import clean_me
from app_utils import clean_all
from app_utils import create_directory
from app_utils import get_model_bin
from app_utils import convertToJPG

from os import path
import torch

import fastai
from deoldify.visualize import *
from pathlib import Path
import traceback


torch.backends.cudnn.benchmark=True

#os.environ['CUDA_VISIBLE_DEVICES']='0'

app = Flask(__name__)


# define a predict function as an endpoint
@app.route("/process-img", methods=["POST"])
def process_image():
    input_path = generate_random_filename(upload_directory,"jpeg")
    output_path = os.path.join(results_img_directory, os.path.basename(input_path))

    try:
        url = request.json["source_url"]
        # render_factor = 35 #int(request.json["render_factor"])

        download(url, input_path)

        run(input_path)

        callback = send_file(output_path, mimetype='image/jpeg')
    
        return callback, 200

    except DownloadPrecheckFailed as e:
        return jsonify({'message': str(e)}), 400
    except:
        traceback.print_exc()
        return jsonify({'message': 'inference error'}), 500

    finally:
        pass
        clean_all([
            input_path,
            output_path
            ])

@app.route("/process-img-form", methods=["POST"])
def processToForm():
    input_path = generate_random_filename(upload_directory,"jpeg")
    output_path = os.path.join(results_img_directory, os.path.basename(input_path))

    image = request.files['image']

    image.save(input_path)

    run(input_path)

    callback = send_file(output_path, mimetype='image/jpeg')
    
    return callback, 200


def run(input_path):
    render_factor = 35

    try:
        image_colorizer.plot_transformed_image(path=input_path, figsize=(20,20),
        render_factor=render_factor, display_render_factor=True, compare=False)
    except:
        convertToJPG(input_path)
        image_colorizer.plot_transformed_image(path=input_path, figsize=(20,20),
        render_factor=render_factor, display_render_factor=True, compare=False)

    return True
    

@app.route('/health')
def health():
    return "ok"

@app.route('/')
def main():
    return app.send_static_file('index.html')
    
if __name__ == '__main__':
    global upload_directory
    global results_img_directory
    global image_colorizer
    #global video_colorizer

    upload_directory = '/data/upload/'
    #create_directory(upload_directory)

    results_img_directory = '/data/result_images/'
    #create_directory(results_img_directory)

    model_directory = '/data/models/'
    #create_directory(model_directory)

    #artistic_model_url = 'https://www.dropbox.com/s/zkehq1uwahhbc2o/ColorizeArtistic_gen.pth?dl=0'
    #get_model_bin(artistic_model_url, os.path.join(model_directory, 'ColorizeArtistic_gen.pth'))

    image_colorizer = get_image_colorizer(artistic=True)


    print('ready for')
    app.run(host='0.0.0.0', port=80, threaded=False)

