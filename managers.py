import pyxel

class BaseManager:
    def __init__(self):
        self.managed_objects = []

    def manage(self):
        pass

    def register_object(self,object):
        self.managed_objects.append(object)

class PhysicsManager(BaseManager):
    def __init__(self):
        super().__init__()    

    def manage(self):
        num_managed_objs = len(self.managed_objects)
        for first_cycle_object_index in range(0,num_managed_objs):
            for second_cycle_object_index in range(0,num_managed_objs):
                self.managed_objects[first_cycle_object_index].process()
                if first_cycle_object_index != second_cycle_object_index:
                    self.managed_objects[first_cycle_object_index].collision(self.managed_objects[second_cycle_object_index])
                

class TickManager(BaseManager):
    def __init__(self):
        super().__init__()

    def manage(self):
        for obj in self.managed_objects:
            obj.tick()

class RenderManager(BaseManager):
    def __init__(self):
        super().__init__()

    def manage(self):
        pyxel.cls(0)
        for obj in self.managed_objects:
            obj.render()

