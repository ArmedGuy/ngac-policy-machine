from .models import Node, NODE_TYPE_PC, NODE_TYPE_UA, NODE_TYPE_OA

class PolicyMachine:
    def __init__(self):
        self.nodes = []
        self.root = Node(NODE_TYPE_PC, 0, {
            "Name": "Policy Machine root"
        })
        self.users_node = Node(NODE_TYPE_UA, -1, {
            "Name": "Users"
        })
        self.root.attach_child(self.users_node)
        self.objects_node = Node(NODE_TYPE_OA, -1, {
            "Name": "Objects"
        })
        self.root.attach_child(self.objects_node)

    @property
    def objects(self):
        return self.objects_node.children

    @property
    def users(self):
        return self.users_node.children
