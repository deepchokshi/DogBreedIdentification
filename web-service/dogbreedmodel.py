# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 19:17:36 2020

@author: DeepChokshi
"""


import tensorflow as tf
import pandas as pd
import numpy as np
import keras

IMAGE_SIZE = 224
labels_csv = pd.read_csv("labels.csv")
labels = labels_csv["breed"].to_numpy()
unique_breeds = np.unique(labels)
BATCH_SIZE = 32

class DogBreed():

    def __init__(self,path):
        self.path = path

    def pre_process_image(image_path):
        #read in a image file
        image = tf.io.read_file(image_path)
        #turn image to numerical tensor with 3 color RGB
        image = tf.image.decode_jpeg(image, channels=3)
        #convert the color channel value from 0-255 to 0-1 value
        image = tf.image.convert_image_dtype(image, tf.float32)
        #resize our image to our desired value (244,244)
        image = tf.image.resize(image, size = [IMAGE_SIZE, IMAGE_SIZE])
        #return the image
        return image

    def get_image_label(image_path,label):
        image = DogBreed.pre_process_image(image_path)
        return image, label

    def create_data_batches(x, y = None, batch_size = BATCH_SIZE, valid_data = False, test_data = False):

      # If the data is the test data set, we don't have labels
        if test_data:
            print('Creating test data batches . . . .')
            data = tf.data.Dataset.from_tensor_slices((tf.constant(x)))   # Only filepaths no labels
            data_batch = data.map(DogBreed.pre_process_image).batch(BATCH_SIZE)
            return data_batch

        # If the data is a valid data set, we don't need to shuffle it
        elif valid_data:
            print("Creating validation data batches . . . ")
            data = tf.data.Dataset.from_tensor_slices((tf.constant(x), tf.constant(y)))
            data_batch = data.map(DogBreed.get_image_label).batch(BATCH_SIZE) #Also preprocesses the images
            return data_batch

        else:
            print("Creating training data batches . . . . ")
            data = tf.data.Dataset.from_tensor_slices((tf.constant(x), tf.constant(y)))
        # Shuffling the pathnames before mapping and processing
            data = data.shuffle(buffer_size = len(x))

            data = data.map(DogBreed.get_image_label)

            data_batch = data.batch(BATCH_SIZE)
        return data_batch


    def get_pred_label(prediction_probabilities):
        return unique_breeds[np.argmax(prediction_probabilities)]

    def load_model(model_path):
        model = keras.models.load_model(model_path)
        return model

    def getbreed(path):
        print("path::: ", path)
        config = tf.compat.v1.ConfigProto(gpu_options = tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=0.8))
        config.gpu_options.allow_growth = True
        session = tf.compat.v1.Session(config=config)
        tf.compat.v1.keras.backend.set_session(session)
        loaded_full_model = DogBreed.load_model("20201102-204119-suffix")
        image_path = [path]
        test_data = DogBreed.create_data_batches(image_path, test_data=True)
        test_predictions = loaded_full_model.predict(test_data,verbose=1)
        return (DogBreed.get_pred_label(test_predictions))
