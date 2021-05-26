import pandas as pd
import numpy as np
import pickle
np.random.seed(1212)
import keras
from keras.models import Model
from keras.layers import *
from keras import optimizers
from keras.layers import Input, Dense
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
from keras.utils.np_utils import to_categorical

def create_model(x_train,y_train):
    model = Sequential()
    model.add(Conv2D(30, (5, 5), input_shape=(28, 28,1), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(15, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(50, activation='relu'))
    model.add(Dense(18, activation='softmax'))
    model.summary()
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=10, batch_size=200,shuffle=True,verbose=1)
    return model
    
dataset=pd.read_csv('dataset.csv')
y_train=dataset['784']
del dataset['784']
dataset=dataset.to_numpy()
row,column =dataset.shape
dataset=np.reshape(dataset,(row,28,28,1))
print(dataset.shape)
y_train=to_categorical(y_train)
model=create_model(dataset,y_train)
model.save('model')

