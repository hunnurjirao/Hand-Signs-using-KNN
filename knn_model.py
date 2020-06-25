import h5py
import os
import cv2
import pickle 
import numpy as np 
from PIL import Image
import matplotlib.pyplot as plt
from sklearn import neighbors


filename_train='hand_signs_datasets\Train_signs.h5'
filename_test='hand_signs_datasets\Test_signs.h5'

f_train = h5py.File(filename_train, 'r')
f_test = h5py.File(filename_test, 'r')


train_images, train_labels = (list(f_train[list(f_train.keys())[1]]), list(f_train[list(f_train.keys())[2]]))
 
test_images, test_labels = (list(f_test[list(f_test.keys())[1]]), list(f_test[list(f_test.keys())[2]]))

class_names=list(f_train[list(f_train.keys())[0]])


train_images=np.array(train_images)
test_images=np.array(test_images)

train_labels=np.array(train_labels)
test_labels=np.array(test_labels)

import keras
train_labels=keras.utils.to_categorical(train_labels,num_classes=6)
test_labels=keras.utils.to_categorical(test_labels,num_classes=6)


train_images=train_images.reshape(1080,-1)
test_images=test_images.reshape(120,-1)


knn = neighbors.KNeighborsClassifier(n_neighbors=5)

knn_model=knn.fit(train_images,train_labels)

accuracy=knn_model.score(test_images,test_labels)

print(accuracy)

saved_model = pickle.dumps(knn_model)
knn_from_pickle = pickle.loads(saved_model)


img=cv2.imread("2.jpg")
im = Image.fromarray(img, 'RGB')

im = im.resize((64,64))
img_array = np.array(im).reshape(1,-1)

pred=knn_from_pickle.predict(img_array) 
print(np.argmax(pred))

