__author__ = 'brad'


class State(object):
    state = 0
    scenes = {}

    def __init__(self):
        return None

    # def __del__(self):
    #     for key in self.scenes.keys():
    #         del self.scenes[key]
    #     del self.scenes

    def add_scene(self, key, scene):
        self.scenes[key] = scene

    def remove_scene(self, key):
        del self.scenes[key]

    def update(self):
        for scene in self.scenes.keys():
            for key in self.scenes[scene].view_update_values.keys():
                self.scenes[scene].update(key, *self.scenes[scene].view_update_values[key])

    def update_collisions(self):
        for key in self.scenes.keys():
            self.scenes[key].update_collisions()