import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QGridLayout, QTableWidget, QTableWidgetItem,
    QSpinBox, QDoubleSpinBox, QPushButton, QLabel, QWidget, QLineEdit, QMessageBox, QComboBox
)
from pyqtgraph import PlotWidget, plot
from scipy.fft import fft
from scipy.io.wavfile import write
import pandas as pd
import pyqtgraph as pg

class Generator:
    def __init__(self, sampleRate, duration):
        self.sampleRate = sampleRate
        self.duration = duration
        self.t = np.linspace(0, duration, int(sampleRate * duration))

    def Sine(self, f, A):
        return A * np.sin(2 * np.pi * f * self.t)

    def Square(self, f, A):
        return A * np.sign(np.sin(2 * np.pi * f * self.t))

    def Sawtooth(self, f, A):
        return A * (2 * (self.t * f - np.floor(self.t * f + 0.5)))

    def Triangle(self, f, A):
        return A * (2 * np.abs(2 * (self.t * f - np.floor(self.t * f + 0.5))) - 1)

    def WhiteNoise(self, A):
        return A * np.random.uniform(-1, 1, len(self.t))

    def FourierTransform(self, data):
        N = len(self.t)
        dt = self.t[1] - self.t[0]
        yf = 2.0 / N * np.abs(fft(data)[0:N // 2])
        xf = np.fft.fftfreq(N, d=dt)[0:N // 2]
        return xf, yf

    def SaveSignalCSV(self, waveform, name):
        data = {"t": self.t, "A": waveform}
        dataframe = pd.DataFrame(data)
        dataframe.to_csv(name + "_signal.csv", index=False, sep="\t")

    def SaveFourierCSV(self, frequencies, amplitudes, name):
        data = {"f": frequencies, "A": amplitudes}
        dataframe = pd.DataFrame(data)
        dataframe.to_csv(name + "_fourier.csv", index=False, sep="\t")

    def SaveWAV(self, waveform, name):
        audio = np.int16(waveform * (2**15))
        write(name, self.sampleRate, audio)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Frequency Analysis")
        self.setGeometry(100, 100, 1200, 675)
        self.generator = Generator(44100, 0.5)
        self.wave = None
        self.fourier = None
        self.initUI()
        self.generate_signal()

    def initUI(self):
        main_layout = QVBoxLayout()
        controls_layout = QGridLayout()
        plots_layout = QHBoxLayout()

        self.signal_type_label = QLabel("Signal Type")
        self.signal_type_combo = QComboBox()
        self.signal_type_combo.addItems([
            "Sine",
            "Square",
            "Sawtooth",
            "Triangle",
            "White Noise"
        ])
        self.signal_type_combo.setCurrentIndex(0)
        self.signal_type_combo.currentIndexChanged.connect(lambda: self.generate_signal())

        self.freq_label = QLabel("Frequency [Hz]:")
        self.freq_spinbox = QDoubleSpinBox()
        self.freq_spinbox.setRange(1, 18000)
        self.freq_spinbox.setValue(440)
        self.freq_spinbox.valueChanged.connect(lambda: self.generate_signal())

        self.amp_label = QLabel("Amplitude:")
        self.amp_spinbox = QDoubleSpinBox()
        self.amp_spinbox.setRange(-10, 10.0)
        self.amp_spinbox.setSingleStep(0.5)
        self.amp_spinbox.setValue(1.0)
        self.amp_spinbox.valueChanged.connect(lambda: self.generate_signal())

        self.sample_rate_label = QLabel("Sampling Frequency [Hz]:")
        self.sample_rate_spinbox = QSpinBox()
        self.sample_rate_spinbox.setRange(1000, 180000)
        self.sample_rate_spinbox.setValue(44100)
        self.sample_rate_spinbox.valueChanged.connect(lambda: self.generate_signal())

        self.duration_label = QLabel("Duration [ms]:")
        self.duration_spinbox = QSpinBox()
        self.duration_spinbox.setRange(1, 1000)
        self.duration_spinbox.setSingleStep(1)
        self.duration_spinbox.setValue(10)
        self.duration_spinbox.valueChanged.connect(lambda: self.generate_signal())

        self.wave_plot = PlotWidget(title="Time Domain Signal")
        self.four_plot = PlotWidget(title="Fourier Transform")

        self.data = QHBoxLayout()

        self.data_table = QTableWidget()
        self.data_table.setColumnCount(2)
        self.data_table.setFixedSize(260, 100)
        self.data_table.setHorizontalHeaderLabels(["Time [s]", "Amplitude"])

        wav = QVBoxLayout()
        self.wav_label = QLabel("Enter WAV file name")
        self.wav_input = QLineEdit()
        self.wav_button = QPushButton("Save signal to WAV")
        self.wav_button.clicked.connect(self.save_wav)
        wav.addWidget(self.wav_label)
        wav.addWidget(self.wav_input)
        wav.addWidget(self.wav_button)

        csv_wave = QVBoxLayout()
        self.csv_wave_label = QLabel("Enter signal CSV file name")
        self.csv_wave_input = QLineEdit()
        self.csv_wave_button = QPushButton("Save signal to CSV")
        self.csv_wave_button.clicked.connect(self.save_csv)
        csv_wave.addWidget(self.csv_wave_label)
        csv_wave.addWidget(self.csv_wave_input)
        csv_wave.addWidget(self.csv_wave_button)

        csv_four = QVBoxLayout()
        self.csv_four_label = QLabel("Enter Fourier CSV file name")
        self.csv_four_input = QLineEdit()
        self.csv_four_button = QPushButton("Save Fourier transform to CSV")
        self.csv_four_button.clicked.connect(self.save_csv_four)
        csv_four.addWidget(self.csv_four_label)
        csv_four.addWidget(self.csv_four_input)
        csv_four.addWidget(self.csv_four_button)

        self.data.addWidget(self.data_table)
        self.data.addLayout(wav)
        self.data.addLayout(csv_wave)
        self.data.addLayout(csv_four)

        controls_layout.addWidget(self.signal_type_label, 0, 0)
        controls_layout.addWidget(self.signal_type_combo, 0, 1)
        controls_layout.addWidget(self.freq_label, 1, 0)
        controls_layout.addWidget(self.freq_spinbox, 1, 1)
        controls_layout.addWidget(self.amp_label, 2, 0)
        controls_layout.addWidget(self.amp_spinbox, 2, 1)
        controls_layout.addWidget(self.sample_rate_label, 3, 0)
        controls_layout.addWidget(self.sample_rate_spinbox, 3, 1)
        controls_layout.addWidget(self.duration_label, 4, 0)
        controls_layout.addWidget(self.duration_spinbox, 4, 1)

        plots_layout.addWidget(self.wave_plot)
        plots_layout.addWidget(self.four_plot)

        main_layout.addLayout(controls_layout)
        main_layout.addLayout(plots_layout)
        main_layout.addLayout(self.data)

        self.setLayout(main_layout)

    def generate_signal(self):
        freq = self.freq_spinbox.value()
        amp = self.amp_spinbox.value()
        sample_rate = self.sample_rate_spinbox.value()
        duration = self.duration_spinbox.value() / 1000

        self.generator = Generator(sample_rate, duration)

        signal_type = self.signal_type_combo.currentIndex()

        match signal_type:
            case 0:
                signal = self.generator.Sine(freq, amp)
            case 1:
                signal = self.generator.Square(freq, amp)
            case 2:
                signal = self.generator.Sawtooth(freq, amp)
            case 3:
                signal = self.generator.Triangle(freq, amp)
            case 4:
                signal = self.generator.WhiteNoise(amp)

        self.wave = signal
        self.wave_plot.clear()
        self.four_plot.clear()

        self.wave_plot.plot(self.generator.t, signal, pen=pg.mkPen(color="r", width=1))

        xf, yf = self.generator.FourierTransform(signal)
        self.fourier = xf, yf

        self.four_plot.plot(xf, yf, pen=pg.mkPen(color="g", width=2))

        self.data_table.setRowCount(len(self.generator.t))
        for i, (t, a) in enumerate(zip(self.generator.t, signal)):
            self.data_table.setItem(i, 0, QTableWidgetItem(f"{t:.6f}"))
            self.data_table.setItem(i, 1, QTableWidgetItem(f"{a:.6f}"))

    def save_csv(self):
        name = self.csv_wave_input.text()
        if name:
            try:
                self.generator.SaveSignalCSV(self.wave, name)
                QMessageBox.information(self, "Success", "CSV file saved")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
        else:
            QMessageBox.critical(self, "Error", "Please fill in the field")

    def save_csv_four(self):
        name = self.csv_four_input.text()
        if name:
            try:
                self.generator.SaveFourierCSV(self.fourier[0], self.fourier[1], name)
                QMessageBox.information(self, "Success", "Fourier transform saved")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
        else:
            QMessageBox.critical(self, "Error", "Please fill in the field")

    def save_wav(self):
        name = self.wav_input.text()
        if name:
            try:
                self.generator.SaveWAV(self.wave, name)
                QMessageBox.information(self, "Success", "WAV file saved")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
        else:
            QMessageBox.critical(self, "Error", "Please fill in the field")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
