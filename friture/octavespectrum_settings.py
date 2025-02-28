#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2009 Timoth?Lecomte

# This file is part of Friture.
#
# Friture is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as published by
# the Free Software Foundation.
#
# Friture is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Friture.  If not, see <http://www.gnu.org/licenses/>.

import logging
import json
from PyQt5 import QtWidgets, QtCore
import json
from friture.subjects_data import subjects_data
import numpy as np
from friture.midi_handler import MidiHandler

# shared with octavespectrum.py
DEFAULT_SPEC_MIN = -80
DEFAULT_SPEC_MAX = 0
DEFAULT_GAIN = 1.0
DEFAULT_WEIGHTING = 0  # None
DEFAULT_BANDSPEROCTAVE = 3
DEFAULT_BANDSPEROCTAVE_INDEX = 1
DEFAULT_RESPONSE_TIME = 1.0
DEFAULT_RESPONSE_TIME_INDEX = 3
DEFAULT_CLASS_1 = 10
DEFAULT_CLASS_2 = 120


class OctaveSpectrum_Settings_Dialog(QtWidgets.QDialog):

    def __init__(self, parent):
        super().__init__(parent)

        self.logger = logging.getLogger(__name__)

        self.setWindowTitle("Octave Spectrum settings")

        self.formLayout = QtWidgets.QFormLayout(self)

        self.comboBox_bandsperoctave = QtWidgets.QComboBox(self)
        self.comboBox_bandsperoctave.setObjectName("comboBox_bandsperoctave")
        self.comboBox_bandsperoctave.addItem("1")
        self.comboBox_bandsperoctave.addItem("3")
        self.comboBox_bandsperoctave.addItem("6")
        self.comboBox_bandsperoctave.addItem("12")
        self.comboBox_bandsperoctave.addItem("24")
        self.comboBox_bandsperoctave.setCurrentIndex(DEFAULT_BANDSPEROCTAVE_INDEX)

        self.spinBox_specmin = QtWidgets.QSpinBox(self)
        self.spinBox_specmin.setKeyboardTracking(False)
        self.spinBox_specmin.setMinimum(-200)
        self.spinBox_specmin.setMaximum(200)
        self.spinBox_specmin.setProperty("value", DEFAULT_SPEC_MIN)
        self.spinBox_specmin.setObjectName("spinBox_specmin")
        self.spinBox_specmin.setSuffix(" dB")

        self.spinBox_specmax = QtWidgets.QSpinBox(self)
        self.spinBox_specmax.setKeyboardTracking(False)
        self.spinBox_specmax.setMinimum(-200)
        self.spinBox_specmax.setMaximum(200)
        self.spinBox_specmax.setProperty("value", DEFAULT_SPEC_MAX)
        self.spinBox_specmax.setObjectName("spinBox_specmax")
        self.spinBox_specmax.setSuffix(" dB")

        self.comboBox_weighting = QtWidgets.QComboBox(self)
        self.comboBox_weighting.setObjectName("weighting")
        self.comboBox_weighting.addItem("None")
        self.comboBox_weighting.addItem("A")
        self.comboBox_weighting.addItem("B")
        self.comboBox_weighting.addItem("C")
        self.comboBox_weighting.setCurrentIndex(DEFAULT_WEIGHTING)

        self.subject1_slider = QtWidgets.QSlider(self)
        self.subject1_slider.setOrientation(QtCore.Qt.Horizontal)
        self.subject1_slider.setObjectName("subject_slider1")
        self.subject1_slider.setMinimum(0)
        self.subject1_slider.setMaximum(100)
        self.subject1_slider.setValue(100)
        self.subject1_slider.setSingleStep(1)

        self.subject2_slider = QtWidgets.QSlider(self)
        self.subject2_slider.setOrientation(QtCore.Qt.Horizontal)
        self.subject2_slider.setObjectName("subject_slider2")
        self.subject2_slider.setMinimum(0)
        self.subject2_slider.setMaximum(100)
        self.subject2_slider.setValue(0)
        self.subject2_slider.setSingleStep(1)

        self.comboBox_response_time = QtWidgets.QSlider(self)
        self.comboBox_response_time.setOrientation(QtCore.Qt.Horizontal)
        self.comboBox_response_time.setObjectName("response_time")
        self.comboBox_response_time.setMinimum(0)
        self.comboBox_response_time.setMaximum(1000)
        self.comboBox_response_time.setValue(
            int(np.log10(DEFAULT_RESPONSE_TIME / 1000))
        )
        self.comboBox_response_time.setSingleStep(1)

        self.gain = QtWidgets.QSlider(self)
        self.gain.setOrientation(QtCore.Qt.Horizontal)
        self.gain.setObjectName("gain")
        self.gain.setMinimum(-1000)  # Adjusted for float representation
        self.gain.setMaximum(1000)  # Adjusted for float representation
        self.gain.setValue(int(DEFAULT_GAIN * 100))  # Convert float to int
        self.gain.setSingleStep(1)

        self.current_classe1 = QtWidgets.QComboBox(self)
        self.current_classe1.setObjectName("soggetto1:")

        self.current_classe2 = QtWidgets.QComboBox(self)
        self.current_classe2.setObjectName("soggetto2:")

        # hardcoded subjects data

        subjects = json.loads(subjects_data)
        for subject in subjects:
            self.current_classe1.addItem(subject + " " + str(subjects[subject]))
            self.current_classe2.addItem(subject + " " + str(subjects[subject]))
        self.current_classe1.setProperty("value", DEFAULT_CLASS_1)
        self.current_classe2.setProperty("value", DEFAULT_CLASS_2)

        self.formLayout.addRow("Bands per octave:", self.comboBox_bandsperoctave)
        self.formLayout.addRow("Max (only UI affected):", self.spinBox_specmax)
        self.formLayout.addRow("Minimum level:", self.spinBox_specmin)
        self.formLayout.addRow("Sensitivity:", self.gain)
        self.formLayout.addRow("Middle-ear weighting:", self.comboBox_weighting)
        self.formLayout.addRow("Response time (ms):", self.comboBox_response_time)
        self.formLayout.addRow("Subject1 (biggan only):", self.current_classe1)
        self.formLayout.addRow("GainSubject1", self.subject1_slider)
        self.formLayout.addRow("Subject2 (biggan only):", self.current_classe2)
        self.formLayout.addRow("GainSubject2", self.subject2_slider)

        self.last_midi_input_label = QtWidgets.QLabel(self)
        self.last_midi_input_label.setObjectName("last_midi_input_label")
        self.last_midi_input_label.setText("Last MIDI Input: None")

        self.formLayout.addRow("Last MIDI Input:", self.last_midi_input_label)

        self.setLayout(self.formLayout)

        self.comboBox_bandsperoctave.currentIndexChanged.connect(
            self.bandsperoctavechanged
        )
        self.spinBox_specmin.valueChanged.connect(self.parent().setmin)
        self.spinBox_specmax.valueChanged.connect(self.parent().setmax)
        self.current_classe1.currentIndexChanged.connect(self.parent().set_class1)
        self.current_classe2.currentIndexChanged.connect(self.parent().set_class2)
        self.gain.valueChanged.connect(self.parent().setgain)
        self.comboBox_weighting.currentIndexChanged.connect(self.parent().setweighting)
        self.comboBox_response_time.valueChanged.connect(self.responsetimechanged)
        self.subject1_slider.valueChanged.connect(self.parent().setratio1)
        self.subject2_slider.valueChanged.connect(self.parent().setratio2)

        self.midi_handler = MidiHandler(self)

    def update_last_midi_input(self, message):
        self.last_midi_input_label.setText(f"Last MIDI Input: {message}")

    # slot
    def bandsperoctavechanged(self, index):
        bandsperoctave = 3 * 2 ** (index - 1) if index >= 1 else 1
        self.logger.info("bandsperoctavechanged slot %d %d", index, bandsperoctave)
        self.parent().setbandsperoctave(bandsperoctave)

    # slot
    def responsetimechanged(self, value):
        response_time = 0.005 + (value / 1000.0) * (
            2.0 - 0.005
        )  # Adjusted to range from 0.005 to 2.0
        self.logger.info("responsetimechanged slot %d %f", value, response_time)
        self.parent().setresponsetime(response_time)

    # method
    def saveState(self, settings):
        settings.setValue("bandsPerOctave", self.comboBox_bandsperoctave.currentIndex())
        settings.setValue("Min", self.spinBox_specmin.value())
        settings.setValue("Max", self.spinBox_specmax.value())
        settings.setValue("weighting", self.comboBox_weighting.currentIndex())
        settings.setValue("response_time", self.comboBox_response_time.value())

    # method
    def restoreState(self, settings):
        bandsPerOctave = settings.value(
            "bandsPerOctave", DEFAULT_BANDSPEROCTAVE_INDEX, type=int
        )
        self.comboBox_bandsperoctave.setCurrentIndex(bandsPerOctave)
        colorMin = settings.value("Min", DEFAULT_SPEC_MIN, type=int)
        self.spinBox_specmin.setValue(colorMin)
        colorMax = settings.value("Max", DEFAULT_SPEC_MAX, type=int)
        self.spinBox_specmax.setValue(colorMax)
        weighting = settings.value("weighting", DEFAULT_WEIGHTING, type=int)
        self.comboBox_weighting.setCurrentIndex(weighting)
        response_time_value = settings.value(
            "response_time", int(np.log10(DEFAULT_RESPONSE_TIME * 1000) * 100), type=int
        )
        self.comboBox_response_time.setValue(response_time_value)

    def closeEvent(self, event):
        self.midi_handler.stop()
        super().closeEvent(event)
