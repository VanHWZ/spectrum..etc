from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtWidgets import *


class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui_MainWindow,self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(300, 200)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.retranslateUi(MainWindow)

        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(120,90,60,20)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("打开")
        MainWindow.setCentralWidget(self.centralWidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton.clicked.connect(self.openfile)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "wav转时域图、频幅图、语谱图"))


    def openfile(self):
        openfile_name = QFileDialog.getOpenFileName(self,'选择文件','','*.wav')
        print(openfile_name[0])
        name = openfile_name[0]
        print(name)
        if name != "":
            import numpy as np
            import wave
            from scipy.fftpack import fft, ifft
            import matplotlib.pyplot as plt

            f = wave.open(name, 'rb')
            params = f.getparams()
            nchannels, sampwidth, framerate, nframes = params[:4]
            strData = f.readframes(nframes)  # 读取音频，字符串格式
            waveData = np.fromstring(strData, dtype=np.int16)  # 将字符串转化为int
            waveData = waveData * 1.0 / (max(abs(waveData)))  # wave幅值归一化
            waveData = np.reshape(waveData, [nframes, nchannels]).T
            data = waveData[0]
            f.close()

            x = np.linspace(0, 1, len(data))
            y = waveData[0]

            yy = fft(y)  # 快速傅里叶变换
            # yreal = yy.real  # 获取实数部分
            # yimag = yy.imag  # 获取虚数部分

            yf = abs(fft(y))  # 取绝对值
            yf1 = abs(fft(y)) / len(y)  # 归一化处理
            yf2 = yf1[range(int(len(y) / 2))]  # 由于对称性，只取一半区间

            xf = np.arange(len(y))  # 频率
            xf1 = xf
            xf2 = xf[range(int(len(y) / 2))]  # 取一半区间

            plt.subplot(221)
            plt.plot(x[0:len(data)], y[0:len(data)])
            plt.title('Original wave')

            # plt.subplot(322)
            # plt.plot(xf, yf, 'r')
            # plt.title('FFT of Mixed wave(two sides frequency range)', fontsize=7, color='#7A378B')  # 注意这里的颜色可以查询颜色代码表
            #
            # plt.subplot(323)
            # plt.plot(xf1, yf1, 'g')
            # plt.title('FFT of Mixed wave(normalization)', fontsize=9, color='r')
            #
            # plt.subplot(324)
            # plt.plot(xf2, yf2, 'b')
            # plt.title('FFT of Mixed wave)', fontsize=10, color='#F08080')

            Fs = 44100  # sampling rate采样率

            n = len(y)  # length of the signal
            k = np.arange(n)
            T = n / Fs
            frq = k / T  # two sides frequency range
            frq1 = frq[range(int(n / 2))]  # one side frequency range

            YY = np.fft.fft(y)  # 未归一化
            Y = np.fft.fft(y) / n  # fft computing and normalization 归一化
            Y1 = Y[range(int(n / 2))]
            YY1 = YY[range(int(n/2))]

            plt.subplot(222)
            plt.plot(frq1, abs(Y1), 'b')  # plotting the spectrum
            plt.xlabel('Freq (Hz)')
            plt.ylabel('|Y(freq)|')

            plt.subplot(223)
            plt.specgram(waveData[0], Fs=framerate, NFFT=1024, noverlap=1000, scale_by_freq=True, sides='default')
            plt.ylabel('Frequency(Hz)')
            plt.xlabel('Time(s)')

            plt.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())



