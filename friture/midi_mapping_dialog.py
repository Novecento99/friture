from PyQt5 import QtWidgets


class MidiMappingDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("MIDI Mapping Settings")

        self.formLayout = QtWidgets.QFormLayout(self)

        self.control_selector = QtWidgets.QComboBox(self)
        self.control_selector.addItems(
            [
                "specmin",
                "specmax",
                "gain",
                "response_time",
                "subject1_slider",
                "subject2_slider",
                "current_classe1",
                "current_classe2",
            ]
        )
        self.control_selector.setObjectName("control_selector")

        self.midi_control_input = QtWidgets.QSpinBox(self)
        self.midi_control_input.setMinimum(0)
        self.midi_control_input.setMaximum(127)
        self.midi_control_input.setObjectName("midi_control_input")

        self.save_button = QtWidgets.QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_mapping)

        self.formLayout.addRow("Control:", self.control_selector)
        self.formLayout.addRow("MIDI Control Number:", self.midi_control_input)
        self.formLayout.addRow(self.save_button)

        self.setLayout(self.formLayout)

    def save_mapping(self):
        control = self.control_selector.currentText()
        midi_control_number = self.midi_control_input.value()
        self.parent().update_midi_mapping(control, midi_control_number)
