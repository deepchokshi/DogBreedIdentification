# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 19:17:36 2020

@author: DeepChokshi
"""

from flask import Flask, request
from dogbreedmodel import DogBreed
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/uploader', methods=['POST'])
def uploader():
    if request.method == 'POST':
        try:
            print("Request::: ", request)
            file = request.files['file']
            print("File::: ", file)
            #check file extenstion
            filePath = os.path.join('upload',file.filename.replace(" ", "_"))
            file.save(filePath)
            breed = DogBreed.getbreed(filePath)
            if(breed):
                return breed
            else:
                return "Cannot predict. Not a dog image", 400
        except:
            return "Internal Server Error", 500

if __name__ == '__main__':
    app.run(debug=True)
