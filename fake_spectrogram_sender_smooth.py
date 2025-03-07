import sys
import time
import random
import socket
import numpy as np
from PyQt5 import QtWidgets, QtCore

# Configuration
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
DEFAULT_BPM = 240
DEFAULT_OFFSET_MS = 0

# Initialize UDP sender
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


class FakeSpectrogramSender(QtCore.QObject):
    def __init__(self):
        super().__init__()
        self.bpm = DEFAULT_BPM
        self.offset_ms = DEFAULT_OFFSET_MS
        self.refresh_spectro = 20
        self.change_time = time.time()
        self.interval = 0.5
        self.refresh_timer = QtCore.QTimer()
        self.refresh_timer.timeout.connect(self.refres_spectrogram)
        self.change_spectrogram_timer = QtCore.QTimer()
        self.change_spectrogram_timer.timeout.connect(self.change_subjects)
        self.click_times = []

        self.gain = 1

        self.last_spectrum = np.random.rand(1000).astype(np.float64)
        self.current_spectro = self.last_spectrum
        self.target_spectrum = np.random.rand(1000).astype(np.float64)
        self.last = time.time()
        self.start()
        self.change_subjects()

        self.refresh_timer.start(self.refresh_spectro)
        self.change_spectrogram_timer.start(int(self.interval * 1000))

        # Send initial subject coast shore
        self.send_initial_subject()

    def send_initial_subject(self):
        subject_1 = 980  # Example subject index for coast
        subject_2 = 2  # Example subject index for shore
        ratio1 = 1.0
        ratio2 = 0.0
        self.send_new_subject(subject_1, subject_2, ratio1, ratio2)

    def send_new_subject(self, subject_1, subject_2, ratio1, ratio2):
        value_ndarray = np.zeros(1000, dtype=np.float64)
        value_ndarray[subject_1] = ratio1
        value_ndarray[subject_2] = ratio2

        # Put a 1 in the first byte to indicate that this is a class
        value_ndarray = np.insert(value_ndarray, 0, 1.0)

        # Convert to bytes
        data = value_ndarray.tobytes()

        sock.sendto(data, (UDP_IP, UDP_PORT))
        print(f"Sent subjects: {subject_1} and {subject_2}")

    def change_subjects(self):
        self.last_spectrum = self.current_spectro
        self.target_spectrum = np.random.rand(1000).astype(np.float64)

        print("Changed subjects", time.time() - self.change_time)
        self.change_time = time.time()

    def refres_spectrogram(self):

        percentage = (time.time() - self.change_time) / (self.interval)
        # print(percentage)
        self.current_spectro = (
            self.last_spectrum * (1 - percentage) + self.target_spectrum * percentage
        )
        # Put a 0 in the first byte to indicate that this is a spectrogram

        data = self.current_spectro * self.gain
        data = np.insert(data, 0, 0.0)

        # Convert to bytes
        data = data.tobytes()

        sock.sendto(data, (UDP_IP, UDP_PORT))

    def set_bpm(self, bpm):
        self.bpm = bpm
        self.interval = 60.0 / self.bpm
        self.change_spectrogram_timer.setInterval(int(self.interval * 1000))
        print(f"BPM set to: {self.bpm}")

    def set_offset(self, offset_ms):
        self.offset_ms = offset_ms
        print(f"Offset set to: {self.offset_ms} ms")

    def set_gain(self, gain):
        self.gain = gain
        print(f"Gain set to: {self.gain}")

    def start(self):
        self.refresh_timer.start(self.refresh_spectro)
        self.change_spectrogram_timer.start(int(self.interval * 1000))
        print("Started")

    def sync(self):
        self.change_subjects()
        self.change_spectrogram_timer.start(int(self.interval * 1000))
        print("Synced")

    def stop(self):
        self.refresh_timer.stop()
        print("Stopped")

    def measure_bpm(self):
        current_time = time.time()
        self.click_times.append(current_time)
        if len(self.click_times) > 1:
            intervals = np.diff(self.click_times)
            avg_interval = np.mean(intervals)
            bpm = 60.0 / avg_interval
            self.set_bpm(bpm)
            # resets timer to sync
            self.change_spectrogram_timer.start(int(self.interval * 1000))
            print(f"Measured BPM: {bpm}")
        if len(self.click_times) > 4:
            self.click_times.pop(0)


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.sender = FakeSpectrogramSender()
        self.sender.start()

        self.bpm_label = QtWidgets.QLabel("BPM:")
        self.bpm_spinbox = QtWidgets.QSpinBox()
        self.bpm_spinbox.setRange(1, 300)
        self.bpm_spinbox.setValue(DEFAULT_BPM)
        self.bpm_spinbox.valueChanged.connect(self.sender.set_bpm)

        self.offset_label = QtWidgets.QLabel("Offset (ms):")
        self.offset_spinbox = QtWidgets.QSpinBox()
        self.offset_spinbox.setRange(-1000, 1000)
        self.offset_spinbox.setValue(DEFAULT_OFFSET_MS)
        self.offset_spinbox.valueChanged.connect(self.sender.set_offset)

        self.gain_label = QtWidgets.QLabel("Gain:")
        self.gain_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.gain_slider.setRange(0, 10)
        self.gain_slider.setValue(1)
        self.gain_slider.valueChanged.connect(self.sender.set_gain)

        self.start_button = QtWidgets.QPushButton("Start")
        self.start_button.clicked.connect(self.sender.start)

        self.stop_button = QtWidgets.QPushButton("Stop")
        self.stop_button.clicked.connect(self.sender.stop)

        self.measure_bpm_button = QtWidgets.QPushButton("Click to Measure BPM")
        self.measure_bpm_button.clicked.connect(self.sender.measure_bpm)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.bpm_label)
        layout.addWidget(self.bpm_spinbox)
        layout.addWidget(self.offset_label)
        layout.addWidget(self.offset_spinbox)
        layout.addWidget(self.gain_label)
        layout.addWidget(self.gain_slider)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.measure_bpm_button)
        self.setLayout(layout)

        self.setWindowTitle("Fake Spectrogram Sender")


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
