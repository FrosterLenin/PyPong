class GameObject:
    def __init__(self, name, x, y, width, height):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def render(self):
        pass
    
    def register_to_managers(self, managers):
        for manager in managers:
            manager.register_object(self)

class PhysicalObject(GameObject):
    def __init__(self, name, x, y, width, height, Yvelocity, Xvelocity):
        super().__init__(name, x, y, width, height)
        self.Yvelocity = Yvelocity
        self.Xvelocity = Xvelocity
        
    def process(self):
        pass
    
    def collision(self, object):
        pass