import numpy as np

class SimulatedBiasDAC:
    def __init__(self, initial_offset=0.0):
        self.offset = initial_offset

    def adjust_offset(self, delta):
        self.offset += delta
        return self.offset
