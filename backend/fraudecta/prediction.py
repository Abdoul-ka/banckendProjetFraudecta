import tensorflow as tf
import numpy as np
from PIL import Image

MODEL = tf.keras.models.load_model('model/modele_diplome.h5')

def predict_image(image_file):
    img = Image.open(image_file).resize((224, 224))
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    pred = MODEL.predict(img)[0][0]
    return float(pred)
