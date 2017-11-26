class Node:
    def __init__(self):
        self.value = {}
        self.children = []

    def __eq__(self, other):
        return self.value == other.value and self.children == other.children
