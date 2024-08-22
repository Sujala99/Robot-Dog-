import numpy as np
import cv2

def sigmoid(x):
    return 1. / (1 + np.exp(-x))

def tanh(x):
    return 2. / (1 + np.exp(-2 * x)) - 1

def preprocess(src_img, size):
    output = cv2.resize(src_img, (size[0], size[1]), interpolation=cv2.INTER_AREA)
    output = output.transpose(2, 0, 1)
    output = output.reshape((1, 3, size[1], size[0])) / 255
    return output.astype('float32')
