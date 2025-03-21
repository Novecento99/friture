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
from friture.midi_mapping_dialog import MidiMappingDialog

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

        self.divisor_slider = QtWidgets.QSlider(self)
        self.divisor_slider.setOrientation(QtCore.Qt.Horizontal)
        self.divisor_slider.setObjectName("divisor_slider")
        self.divisor_slider.setMinimum(1)
        self.divisor_slider.setMaximum(1000)
        self.divisor_slider.setValue(1)
        self.divisor_slider.setSingleStep(1)

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
        self.formLayout.addRow("Divisor:", self.divisor_slider)

        self.midi_input_selector = QtWidgets.QComboBox(self)
        self.midi_input_selector.setObjectName("midi_input_selector")
        self.refresh_midi_inputs_button = QtWidgets.QPushButton(
            "Refresh MIDI Inputs", self
        )
        self.refresh_midi_inputs_button.setObjectName("refresh_midi_inputs_button")

        self.formLayout.addRow("MIDI Input Device:", self.midi_input_selector)
        self.formLayout.addRow(self.refresh_midi_inputs_button)

        self.last_midi_input_label = QtWidgets.QLabel(self)
        self.last_midi_input_label.setObjectName("last_midi_input_label")
        self.last_midi_input_label.setText("Last MIDI Input: None")

        self.formLayout.addRow("Last MIDI Input:", self.last_midi_input_label)

        self.midi_mapping_button = QtWidgets.QPushButton("MIDI Mapping Settings", self)
        self.midi_mapping_button.setObjectName("midi_mapping_button")

        self.formLayout.addRow(self.midi_mapping_button)

        self.autoChangeSubjectCheckbox = QtWidgets.QCheckBox(
            "Auto Change Subject", self
        )
        self.autoChangeSubjectCheckbox.setObjectName("autoChangeSubjectCheckbox")
        self.autoChangeSubjectCheckbox.stateChanged.connect(
            self.toggle_auto_change_subject
        )
        self.formLayout.addRow("Auto Change Subject:", self.autoChangeSubjectCheckbox)

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
        self.midi_input_selector.currentIndexChanged.connect(self.change_midi_input)
        self.refresh_midi_inputs_button.clicked.connect(self.refresh_midi_inputs)
        self.midi_mapping_button.clicked.connect(self.open_midi_mapping_dialog)
        self.divisor_slider.valueChanged.connect(self.parent().set_divisor)

        self.midi_handler = MidiHandler(self)
        self.refresh_midi_inputs()

    def open_midi_mapping_dialog(self):
        dialog = MidiMappingDialog(self)
        dialog.exec_()

    def update_midi_mapping(self, control, midi_control_number):
        self.midi_handler.update_mapping(control, midi_control_number)

    def update_last_midi_input(self, message):
        self.last_midi_input_label.setText(f"Last MIDI Input: {message}")

    def refresh_midi_inputs(self):
        self.midi_input_selector.clear()
        available_ports = self.midi_handler.get_available_ports()
        self.midi_input_selector.addItems(available_ports)

    def change_midi_input(self, index):
        selected_port = self.midi_input_selector.currentText()
        self.midi_handler.change_midi_input(selected_port)

    def toggle_auto_change_subject(self, state):
        self.parent().auto_change_subject = state == QtCore.Qt.Checked
        print(f"Auto Change Subject: {self.parent().auto_change_subject}")

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
