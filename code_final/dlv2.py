# Import Libraries
import numpy as np 
import sqlite3
from matplotlib import image

# file system libraries
import os
import os.path

# confusion matrix
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report  

# Images, Plotting
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# tensorflow - CNNs
import tensorflow as tf
import keras.backend as K
from tensorflow import keras
from tensorflow.keras.models import Model, load_model
from tensorflow.keras import backend, models, layers, Sequential
from tensorflow.keras.layers import Input, Concatenate, Dense, Dropout, Flatten, Add
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping,ReduceLROnPlateau
from tensorflow.keras.applications import DenseNet121,InceptionV3, Xception, ResNet101
from keras_tuner.tuners import Hyperband

def f1_score(y_true, y_pred): #taken from old keras source code
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    recall = true_positives / (possible_positives + K.epsilon())
    f1_val = 2*(precision*recall)/(precision+recall+K.epsilon())
    return f1_val

def accuracy (y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    true_negatives = K.sum(K.round(K.clip((1 - y_true)*(1 - y_pred), 0, 1)))
    false_positives = K.sum(K.round(K.clip((1 - y_true)*(y_pred), 0, 1)))
    false_negatives = K.sum(K.round(K.clip((y_true)*(1 - y_pred), 0, 1)))
    acc_val = ((true_positives + true_negatives)/(true_positives + true_negatives + false_positives + false_negatives))
    return acc_val

# Constants
# Constants
FOLDERS     = ['Alzheimer_s Dataset','patients']
DIR_INPUT   = '/content/drive/MyDrive/Pathologia/Alzheimer'
DIR_WORK    = './'
DIR_MODELS  = os.path.join('/content/drive/MyDrive/Pathologia/Modèles/','models')
DIR_PATIENTS   = os.path.join('/content/drive/MyDrive/Pathologia/Alzheimer/Alzheimer_s Dataset/Recherche_alzheimer_patients')
CLASS_LIST  = ['Recherche', 'Archive']

# Set seeds for reproducibility 
SEED        = 1985
tf.random.set_seed(SEED)
np.random.seed(SEED)

IMG_SIZE = [176,208]
BATCH_SIZE = 32

# Scale Images
patients_images  = ImageDataGenerator(rescale  = 1./255)

# Image Generators
patients_gen = patients_images.flow_from_directory(
    DIR_PATIENTS,
    target_size = IMG_SIZE,
    batch_size  = BATCH_SIZE,
    class_mode  = 'categorical',
    color_mode  = 'rgb',
    seed        = SEED,
    shuffle     = False
)

chargement_modele = load_model('/content/drive/MyDrive/Pathologia/Modèles/models/DenseNet121_model_added_capacity.keras',custom_objects={"f1_score": f1_score, "accuracy" : accuracy})

pred = chargement_modele.predict(patients_gen)

conn = sqlite3.connect('/content/drive/MyDrive/db.sqlite3', timeout=10)

conn.execute("INSERT INTO webapp_result (Id_Patient, Prediction, Type) VALUES ('DP1',"+str(pred[0,1])+", 'DP')")

conn.commit()
conn.close()