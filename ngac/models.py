
class Operation:
    def __init__(self):
        self.name = None
        self.description = None


NODE_TYPE_C = "Connector"
NODE_TYPE_PC = "Policy Class"
NODE_TYPE_UA = "User Attribute"
NODE_TYPE_U = "User"
NODE_TYPE_OA = "Object Attribute"
NODE_TYPE_O = "Object"
NODE_TYPE_OS = "Operation Set"

class Node:
    def __init__(self, node_type, id, data):
        self.node_type = node_type
        self.id = id
        self.data = data
        self.parents = []
        self.children = []

    def __str__(self):
        return "<{} {}>".format(self.node_type, self.id)
    
    def attach_child(self, child):
        self.children.append(child)
        child.parents.append(self)

    def detach_child(self, child):
        child.parents.remove(self)
        self.children.remove(child)

    def get_inheritance_chain(self):
        """
        Return a list of nodes that this node inherits from
        """
        nodes = [self]
        for p in self.parents:
            nodes += p.get_inheritance_chain()
        return set(nodes)