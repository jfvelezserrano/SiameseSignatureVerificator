"""
    Moudlo que permite verificar firmas.
"""

import os
import cv2
import numpy as np
import keras
JSON_2_MODEL = keras.models.model_from_json

#from tensorflow.keras.models import model_from_json

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = ""

class SignatureVerificator:
    """
        Clase que permite verificar firmas.
    """

    def __init__(self):
        """
            COnstructor que carga la red.
        """
        json_file = open('the_very_best_inception_model.json', 'r')
        json_model = json_file.read()
        json_file.close()
        self.model = JSON_2_MODEL(json_model)
        self.model.load_weights("the_very_best_inception_model.hdf5")            

    def verify(self, undibitated_signature_img: np.array, dubitated_signature_img: np.array)->float:
        """
            Método que verifica firmas.
            Devuelve un número real con valor entre 0 (no se parece) y 1 (separece)
            UNDUBITATED_SIGNATURE_IMG : Imagen de una firma modelo en niveles de gris [0,255].
            DUBITATED_SIGNATURE_IMG : Imagen de una firma en duda en niveles de gris [0,255].
        """

        undibitated_signature_img = self.__homogenizar(undibitated_signature_img, (128, 128))
        undibitated_signature_img = undibitated_signature_img.reshape((1, 128, 128, 1))

        dubitated_signature_img = self.__homogenizar(dubitated_signature_img, (128, 128))
        dubitated_signature_img = dubitated_signature_img.reshape((1, 128, 128, 1))

        output = self.model.predict([undibitated_signature_img, dubitated_signature_img])
        return output[0, 0]

    @staticmethod
    def __homogenizar(img, size):
        """
            Recibe una imagen gris tipo byte.
            Devuelve una imagen gris tipo byte.
            Devuelve una imagen del tamaño especificado, que contiene la que se le pasa.
            Adapta la imagen para ocupar el mayor area posible.
        """

        th,img = cv2.threshold(img,0,255,type=cv2.THRESH_OTSU+cv2.THRESH_BINARY)
        kernel = np.ones((5,5), np.uint8)
        img = cv2.erode(img,kernel)

        img_copy = 255 - img

        contours = cv2.findContours(img_copy,cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_SIMPLE)
        
        all_contours = np.empty((0,1,2),dtype=int)

        for contour in contours[1]:
            all_contours = np.concatenate((all_contours,contour))
        
        (x,y,w,h) = cv2.boundingRect(all_contours)
        img = img[y:y+h,x:x+w]

        fondo = np.ones((size[0], size[1]), np.uint8)
        fondo *= 255
        if img.shape[0] > img.shape[1]:
            new_hight = size[0]
            new_width = img.shape[1] * size[0] // img.shape[0]

            new_img = cv2.resize(img, (new_width, new_hight), interpolation=cv2.INTER_LINEAR)

            centronew_img = new_width // 2
            centrofondo = fondo.shape[1] // 2

            ini = (centrofondo - centronew_img)
            fin = ini + new_width
            fondo[0:new_img.shape[0], ini:fin] = new_img
        else:

            new_hight = img.shape[0] * size[0] // img.shape[1]
            new_width = size[0]

            new_img = cv2.resize(img, (new_width, new_hight), interpolation=cv2.INTER_LINEAR)

            centronew_img = new_hight // 2
            centrofondo = fondo.shape[0] // 2
            ini = (centrofondo - centronew_img)
            fin = ini + new_hight
            fondo[ini:fin, 0:new_img.shape[1]] = new_img
        fondo = fondo.reshape(size) / 255.0
        return fondo
