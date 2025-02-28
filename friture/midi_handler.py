import mido
import logging


class MidiHandler:
    def __init__(self, octave_spectrum_settings_dialog):
        self.dialog = octave_spectrum_settings_dialog
        self.logger = logging.getLogger(__name__)
        self.running = False
        self.midi_input = None
        self.mappings = {
            1: "specmin",
            2: "specmax",
            3: "gain",
            4: "response_time",
            5: "subject1_slider",
            6: "subject2_slider",
            7: "current_classe1",
            8: "current_classe2",
        }

        self.initialize_midi_input()

    def initialize_midi_input(self):
        try:
            available_ports = mido.get_input_names()
            if not available_ports:
                raise OSError("no ports available")

            self.midi_input = mido.open_input(callback=self.midi_callback)
            self.running = True
            self.logger.info(f"MIDI input initialized: {available_ports}")
        except OSError as e:
            self.logger.warning(f"MIDI input initialization failed: {e}")

    def get_available_ports(self):
        return mido.get_input_names()

    def change_midi_input(self, port_name):
        if self.midi_input:
            self.midi_input.close()
        self.midi_input = mido.open_input(port_name, callback=self.midi_callback)
        self.logger.info(f"Changed MIDI input to: {port_name}")

    def update_mapping(self, control, midi_control_number):
        self.mappings[midi_control_number] = control
        self.logger.info(f"Updated MIDI mapping: {midi_control_number} -> {control}")

    def midi_callback(self, message):
        if message.type == "control_change":
            control = message.control
            value = message.value
            if control in self.mappings:
                mapped_control = self.mappings[control]
                if mapped_control == "specmin":
                    self.dialog.spinBox_specmin.setValue(value - 100)  # Adjust range
                elif mapped_control == "specmax":
                    self.dialog.spinBox_specmax.setValue(value - 100)  # Adjust range
                elif mapped_control == "gain":
                    self.dialog.gain.setValue(value * 10 - 1000)  # Adjust range
                elif mapped_control == "response_time":
                    self.dialog.comboBox_response_time.setValue(value)  # Adjust range
                elif mapped_control == "subject1_slider":
                    self.dialog.subject1_slider.setValue(value)
                elif mapped_control == "subject2_slider":
                    self.dialog.subject2_slider.setValue(value)
                elif mapped_control == "current_classe1":
                    self.dialog.current_classe1.setCurrentIndex(value)
                elif mapped_control == "current_classe2":
                    self.dialog.current_classe2.setCurrentIndex(value)

        self.dialog.update_last_midi_input(message)

    def stop(self):
        if self.running:
            self.running = False
            if self.midi_input:
                self.midi_input.close()
