#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2009 Timothée Lecomte

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

from PyQt5 import QtCore
import numpy as np
from friture.ringbuffer import RingBuffer

FRAMES_PER_BUFFER = 1024


class AudioBuffer(QtCore.QObject):
    new_data_available = QtCore.pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()

        self.ringbuffer = RingBuffer()
        self.newpoints = 0
        self.lastDataTime = 0.

    def data(self, length):
        return self.ringbuffer.data(length)

    def data_older(self, length, delay_samples):
        return self.ringbuffer.data_older(length, delay_samples)

    def newdata(self):
        return self.data(self.newpoints)

    def set_newdata(self, newpoints):
        self.newpoints = newpoints

    def data_indexed(self, start, length):
        return self.ringbuffer.data_indexed(start, length)
    
    def data_time(self, start: int) -> float:
        """The stream time in seconds at the position defined by 'start'."""
        return self.ringbuffer.data_time(start)

    def handle_new_data(self, floatdata: np.ndarray, input_time: float, status) -> None:
        self.ringbuffer.push(floatdata, input_time)
        self.set_newdata(floatdata.shape[1])
        self.new_data_available.emit(floatdata)
        self.lastDataTime = input_time
