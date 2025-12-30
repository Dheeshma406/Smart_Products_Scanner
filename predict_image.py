import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

IMG_SIZE = 128  # MUST match training

model = tf.keras.models.load_model("product_model.keras")

class_names = [
    'Amul_Milk','Chakra_Gold','Colgate_Paste','Colgate_Tooth_Brush',
    'Dettol','Dove_Soap','Fortune_Oil','Harpic','Himalaya_Shamapoo',
    'Lizol','Lux_Soap','Maggi_Noodles','Milky_Bikis',
    'Nestle_Milk_Powder','Parachute_Oil','Plastic_Bottle',
    'Pril_Liquid','Tata_Salt','Yardley_Powder'
]

def predict_product(img_path):
    img = image.load_img(img_path, target_size=(IMG_SIZE, IMG_SIZE))
    img = image.img_to_array(img)
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    preds = model.predict(img)
    index = np.argmax(preds)
    confidence = float(np.max(preds))

    return class_names[index], confidence
