# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'aula3.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.metrics import accuracy_score

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QApplication

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(709, 307)

        self.path = ''

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.xray = QtWidgets.QLabel(self.centralwidget)
        self.xray.setGeometry(QtCore.QRect(10, 10, 311, 251))
        self.xray.setText("")
        self.xray.setPixmap(QtGui.QPixmap("../DIAGNOSIS/dataset/pneumonia/test/normal/IM-0003-0001.jpeg"))
        self.xray.setScaledContents(True)
        self.xray.setObjectName("xray")

        self.btnLoad = QtWidgets.QPushButton(self.centralwidget)
        self.btnLoad.setGeometry(QtCore.QRect(10, 270, 105, 31))
        self.btnLoad.setObjectName("btnLoad")
        self.btnLoad.clicked.connect(self.loadImage)

        self.btnLaudar = QtWidgets.QPushButton(self.centralwidget)
        self.btnLaudar.setGeometry(QtCore.QRect(120, 270, 105, 31))
        self.btnLaudar.setObjectName("btnLoad")
        self.btnLaudar.clicked.connect(self.result)

        self.btnSair = QtWidgets.QPushButton(self.centralwidget)
        self.btnSair.setGeometry(QtCore.QRect(230, 270, 91, 31))
        self.btnSair.setObjectName("btnSair")
        self.btnSair.clicked.connect(self.closeApp)

        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(330, 10, 20, 291))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(350, 10, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setStyleSheet("color: \"red\"")
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(350, 70, 351, 131))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(20)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setStyleSheet("color: \"green\"")
        self.label_2.setObjectName("label_2")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle("DIAGNOSIS")
        self.btnLoad.setText(_translate("MainWindow", "Carregar Exame"))
        self.btnLaudar.setText("Examinar")
        self.btnSair.setText(_translate("MainWindow", "Sair"))
        self.label.setText(_translate("MainWindow", "Resultado:"))
        self.label_2.setText("ESCOLHA UM EXAME")

    def loadImage(self):
        self.path = QFileDialog.getOpenFileName()[0]
        self.xray.setPixmap(QtGui.QPixmap(self.path))
        self.preparar()

    def preparar(self):
        self.btnLoad.setEnabled(False)
        self.btnSair.setEnabled(False)

        self.label_2.setStyleSheet("color: \"blue\"")
        self.label_2.setText("EXECUTE O EXAME")

    def result(self):
        self.label_2.setStyleSheet("color: \"blue\"")
        self.label_2.setText("AGUARDE O EXAME")

        train_datagen = ImageDataGenerator(preprocessing_function=tf.keras.applications.resnet50.preprocess_input,
                                           rotation_range=50,
                                           width_shift_range=0.2,
                                           height_shift_range=0.2,
                                           zoom_range=0.1,
                                           horizontal_flip=True,
                                           vertical_flip=True)

        train_generator = train_datagen.flow_from_directory('../DIAGNOSIS/dataset/pneumonia/train',
                                                            target_size=(224, 224),
                                                            batch_size=2,
                                                            class_mode='categorical',
                                                            shuffle=True)

        test_datagen = ImageDataGenerator(preprocessing_function=tf.keras.applications.resnet50.preprocess_input)

        test_generator = test_datagen.flow_from_directory('../DIAGNOSIS/dataset/pneumonia/test',
                                                          target_size=(224, 224),
                                                          batch_size=1,
                                                          class_mode='categorical',
                                                          shuffle=False)

        model = load_model('model.h5')
        filenames = test_generator.filenames
        predictions = model.predict_generator(test_generator, steps=len(filenames))
        predictions2 = []

        for i in range(len(predictions)):
            predictions2.append(np.argmax(predictions[i]))

        accuracy_score(predictions2, test_generator.classes)
        amostra = self.path
        image = tf.keras.preprocessing.image.load_img(r'' + amostra, target_size=(224, 224))

        image = tf.keras.preprocessing.image.img_to_array(image)
        np.shape(image)

        np.max(image), np.min(image)

        image = np.expand_dims(image, axis=0)
        np.shape(image)
        image = tf.keras.applications.resnet50.preprocess_input(image)
        np.max(image), np.min(image)
        predictions = model.predict(image)
        prediction = list(train_generator.class_indices)[np.argmax(predictions[0])]

        if prediction == "bacteriana":
            self.label_2.setStyleSheet("color: \"orange\"")
            self.label_2.setText("PNEUMONIA BACTERIANA")

        if prediction == "normal":
            self.label_2.setStyleSheet("color: \"green\"")
            self.label_2.setText("PULMÃO SEM ANOMALIAS")

        if prediction == "viral":
            self.label_2.setStyleSheet("color: \"red\"")
            self.label_2.setText("PNEUMONIA VIRAL")

        self.btnLoad.setEnabled(True)
        self.btnLaudar.setEnabled(True)
        self.btnSair.setEnabled(True)

        return prediction

    def closeApp(self):
        QApplication.quit()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

