class Component:
    def __init__(self, name, block):
        self.name = name
        self.block = block

    def to_pair(self):
        return self.name, self.block()
