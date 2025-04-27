from common.config_loader import ConfigLoader
import os

class SaveManager:
    def __init__(self, save_name='save', default_save=None):
        self.save_name = save_name
        self.default_save = default_save or {}
        self.loader = ConfigLoader(save_name, self.default_save)
        self.save_data = None

    def load(self):
        self.save_data = self.loader.load()
        return self.save_data

    def save(self, data=None):
        if data is not None:
            self.save_data = data
        if self.save_data is None:
            self.save_data = self.default_save.copy()
        return self.loader.save(self.save_data)

    def get(self, key, default=None):
        if self.save_data is None:
            self.load()
        return self.save_data.get(key, default)

    def set(self, key, value):
        if self.save_data is None:
            self.load()
        self.save_data[key] = value
        self.save(self.save_data) 