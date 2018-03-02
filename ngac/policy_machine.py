from .models import Node, NODE_TYPE_PC, NODE_TYPE_UA, NODE_TYPE_OA

class PolicyMachine:
    def __init__(self):
        self.nodes = []
        self.associations = []

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

        self.nodes.append(self.root)
        self.nodes.append(self.objects_node)
        self.nodes.append(self.users_node)

    def attach_node(self, parent, node):
        self.nodes.append(node)
        parent.attach_child(node)

    def add_association(self, association):
        self.associations.append(association)

    def is_allowed(self, ua_id, operation, oa_id):
        """
        :param ua_id. A user or user attribute id to calculate access rights from.
        :param operation. The operation to check if it is allowed.
        :param oa_id. An object or object attribute that access rights are calculated against.
        """

        ua = [x for x in self.nodes if x.id == ua_id].pop()
        oa = [x for x in self.nodes if x.id == oa_id].pop()

        if not ua or not oa:
            return False
        
        #print("Check on", ua, oa)

        user_attributes = ua.get_inheritance_chain()
        object_attributes = oa.get_inheritance_chain()

        #print("User attribute chain", user_attributes)
        #print("Object attribute chain", object_attributes)

        for ass_ua, _, ass_oa in [x for x in self.associations if x[1] == operation]:
            #print("Match found in matching operation", ass_ua, ass_oa)
            if ass_ua in user_attributes and ass_oa in object_attributes:
                return True
        return False
