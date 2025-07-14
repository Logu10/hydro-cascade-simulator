import json
from typing import List
import pandas as pd

RHO = 1000
G = 9.81
MIN_FLOW = 20  # m³/s, environmental

class ReservoirPlant:
    def __init__(self, cfg):
        self.name = cfg['name']
        self.head = cfg['head']
        self.eff = cfg['efficiency']
        self.max_flow = cfg['max_flow']
        self.capacity = cfg['storage_capacity']
        self.storage = cfg['initial_storage']
        self.history = {'release': [], 'storage': [], 'power_mw': []}

    def step(self, inflow):
        self.storage = min(self.storage + inflow, self.capacity)
        avail = self.storage
        release = max(min(avail, self.max_flow), MIN_FLOW)
        self.storage -= release
        power = self.eff * RHO * G * release * self.head / 1e6
        self.history['release'].append(release)
        self.history['storage'].append(self.storage)
        self.history['power_mw'].append(power)
        return release