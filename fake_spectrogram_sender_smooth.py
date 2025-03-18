import sys
import time
import random
import socket
import numpy as np
from PyQt5 import QtWidgets, QtCore

# Configuration
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
DEFAULT_BPM = 100
DEFAULT_OFFSET_MS = 0

# Initialize UDP sender
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


class FakeSpectrogramSender(QtCore.QObject):
    def __init__(self):
        super().__init__()
        self.bpm = DEFAULT_BPM
        self.offset_ms = DEFAULT_OFFSET_MS

        self.refresh_liumotion = 20
        self.counter = 1

        self.noise_change_time = time.time()
        self.noise_change_interval = 0.5

        self.subjects_change_time = time.time()
        self.subject_change_interval = self.noise_change_interval * 4

        self.refresh_timer = QtCore.QTimer()
        self.refresh_timer.timeout.connect(self.update_liumotion)
        self.change_spectrogram_timer = QtCore.QTimer()
        self.change_spectrogram_timer.timeout.connect(self.new_noise_target)
        self.change_subject_timer = QtCore.QTimer()
        self.change_subject_timer.timeout.connect(self.nothing)
        self.click_times = []

        self.gain = 1.0

        self.last_noise = np.random.rand(1000).astype(np.float64)
        self.current_noise = self.last_noise
        self.target_noise = np.random.rand(1000).astype(np.float64)

        self.last_subjects = np.zeros(1000, dtype=np.float64)
        self.current_subjects = self.last_subjects
        self.target_subjects = np.zeros(1000, dtype=np.float64)

        self.start()
        self.new_noise_target()
        self.new_subject_target()

        self.refresh_timer.start(self.refresh_liumotion)
        self.change_spectrogram_timer.start(int(self.noise_change_interval * 1000))
        self.change_subject_timer.start(int(self.subject_change_interval * 1000))

        self.coeff = 0.8

    def nothing(self):
        pass

    def new_subject_target(self):
        self.last_subjects = self.current_subjects
        value_ndarray = np.zeros(1000, dtype=np.float64)  # Initialize with zeros
        x_subject = random.randint(0, 999)
        value_ndarray[x_subject] = 1

        self.target_subjects = value_ndarray

        print("Changed subjects", time.time() - self.subjects_change_time)
        self.subjects_change_time = time.time()

    def new_noise_target(self):
        self.counter += 1
        if self.counter % 4 == 0:
            self.new_subject_target()
        self.last_noise = self.current_noise
        self.target_noise = np.random.rand(1000).astype(np.float64)

        print("Changed noise", time.time() - self.noise_change_time)
        self.noise_change_time = time.time()

    def elastic_lerp(self, t):
        # 0.5+0.5*cot(coeff*pi/2)*tan(coeff*pi*(t-0.5))
        if self.coeff == 0:
            return t
        val = 0.5 + 0.5 * (1 / np.tan(self.coeff * np.pi / 2)) * np.tan(
            self.coeff * np.pi * (t - 0.5)
        )
        return val

    def update_liumotion(self):

        percentage_noise = (time.time() - self.noise_change_time) / (
            self.noise_change_interval
        )
        percentage_noise = self.elastic_lerp(percentage_noise)
        self.current_noise = (
            self.last_noise * (1 - percentage_noise)
            + self.target_noise * percentage_noise
        )
        # Put a 0 in the first byte to indicate that this is a spectrogram

        data = self.current_noise * self.gain
        data = np.insert(data, 0, 0.0)

        # Convert to bytes
        data = data.tobytes()

        sock.sendto(data, (UDP_IP, UDP_PORT))

        percentage_subjects = (time.time() - self.subjects_change_time) / (
            self.subject_change_interval
        )
        # percentage_subjects = self.elastic_lerp(percentage_subjects)
        self.current_subjects = (
            self.last_subjects * (1 - percentage_subjects)
            + self.target_subjects * percentage_subjects
        )
        data = self.current_subjects
        # Put a 1 in the first byte to indicate that this is a subject
        data = np.insert(data, 0, 1.0)
        # data has to be float64
        data = data.astype(np.float64)
        # Convert to bytes
        data = data.tobytes()
        sock.sendto(data, (UDP_IP, UDP_PORT))

    def set_bpm(self, bpm):
        self.bpm = bpm
        self.noise_change_interval = 60.0 / self.bpm
        self.change_spectrogram_timer.setInterval(
            int(self.noise_change_interval * 1000)
        )
        print(f"BPM set to: {self.bpm}")

    def set_offset(self, offset_ms):
        self.offset_ms = offset_ms
        print(f"Offset set to: {self.offset_ms} ms")

    def set_gain(self, gain):
        self.gain = gain / 100.0
        print(f"Gain set to: {self.gain}")

    def set_coeff(self, coeff):
        self.coeff = coeff / 100.0
        print(f"Coeff set to: {self.coeff}")

    def start(self):
        print("refresh_timer started")
        self.refresh_timer.start(self.refresh_liumotion)
        print("change_spectrogram_timer started")
        self.change_spectrogram_timer.start(int(self.noise_change_interval * 1000))
        print("change_subject_timer started")
        self.change_subject_timer.start(int(self.subject_change_interval * 1000))
        print("Started")

    def sync(self):
        self.new_noise_target()
        self.new_subject_target()
        self.change_subject_timer.start(int(self.subject_change_interval * 1000))
        self.change_spectrogram_timer.start(int(self.noise_change_interval * 1000))

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
            self.parent().bpm_spinbox.setValue(
                int(bpm)
            )  # Update the spinbox with the measured BPM

            # resets timer to sync
            self.change_spectrogram_timer.start(int(self.noise_change_interval * 1000))
            self.change_subject_timer.start(int(self.subject_change_interval * 1000))
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
        self.sender.parent = (
            lambda: self
        )  # Set the parent function to return this MainWindow instance

        self.offset_label = QtWidgets.QLabel("Offset (ms):")
        self.offset_spinbox = QtWidgets.QSpinBox()
        self.offset_spinbox.setRange(-1000, 1000)
        self.offset_spinbox.setValue(DEFAULT_OFFSET_MS)
        self.offset_spinbox.valueChanged.connect(self.sender.set_offset)

        self.gain_label = QtWidgets.QLabel("Gain:")
        self.gain_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.gain_slider.setRange(0, 1000)  # Adjusted for 0.01 precision
        self.gain_slider.setValue(100)
        self.gain_slider.valueChanged.connect(self.sender.set_gain)

        self.coeff_label = QtWidgets.QLabel("Coeff:")
        self.coeff_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.coeff_slider.setRange(0, 100)  # Adjusted for 0.01 precision
        self.coeff_slider.setValue(80)
        self.coeff_slider.valueChanged.connect(self.sender.set_coeff)

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
        layout.addWidget(self.coeff_label)
        layout.addWidget(self.coeff_slider)
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
