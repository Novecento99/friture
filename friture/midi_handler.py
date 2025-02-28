import mido
from threading import Thread
import logging


class MidiHandler:
    def __init__(self, octave_spectrum_settings_dialog):
        self.dialog = octave_spectrum_settings_dialog
        self.logger = logging.getLogger(__name__)
        self.running = False
        self.midi_input = None

        self.initialize_midi_input()

    def initialize_midi_input(self):
        try:
            available_ports = mido.get_input_names()
            if not available_ports:
                raise OSError("no ports available")

            self.midi_input = mido.open_input(callback=self.midi_callback)
            self.running = True
            self.thread = Thread(target=self.listen)
            # self.thread.start()
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

    def listen(self):
        while self.running:
            pass

    def midi_callback(self, message):
        if message.type == "control_change":
            control = message.control
            value = message.value
            if control == 1:  # Example control number for specmin
                self.dialog.spinBox_specmin.setValue(value - 100)  # Adjust range
            elif control == 2:  # Example control number for specmax
                self.dialog.spinBox_specmax.setValue(value - 100)  # Adjust range
            elif control == 3:  # Example control number for gain
                self.dialog.gain.setValue(value * 10 - 1000)  # Adjust range
            elif control == 4:  # Example control number for response time
                self.dialog.comboBox_response_time.setValue(value)  # Adjust range
            elif control == 5:  # Example control number for subject1 slider
                self.dialog.subject1_slider.setValue(value)
            elif control == 6:  # Example control number for subject2 slider
                self.dialog.subject2_slider.setValue(value)

        self.dialog.update_last_midi_input(message)

    def stop(self):
        if self.running:
            self.running = False
            # self.thread.join()
            if self.midi_input:
                self.midi_input.close()
