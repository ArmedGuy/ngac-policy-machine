from .models import Node, NODE_TYPE_PC, NODE_TYPE_UA, NODE_TYPE_OA
import sys

class PolicyMachine:
    def __init__(self):
        self.nodes = []
        self.associations = []

        self.root = Node(NODE_TYPE_PC, "pm_root", {
            "Name": "Policy Machine root"
        })
        self.users_node = Node(NODE_TYPE_UA, "pm_users", {
            "Name": "Users"
        })
        self.root.attach_child(self.users_node)
        self.objects_node = Node(NODE_TYPE_OA, "pm_objects", {
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

        first = lambda l: next(iter(l), None)
        
        ua = first(x for x in self.nodes if x.id == ua_id)
        oa = first(x for x in self.nodes if x.id == oa_id)

        if not ua or not oa:
            return False
        
        #print("Check on", ua, oa, file=sys.stderr)

        user_attributes = [x.id for x in ua.get_inheritance_chain()]
        object_attributes = [x.id for x in oa.get_inheritance_chain()]

        #print("User attribute chain", [str(x) for x in user_attributes], file=sys.stderr)
        #print("Object attribute chain", [str(x) for x in object_attributes], file=sys.stderr)

        for ass_ua, _, ass_oa in [x for x in self.associations if x[1] == operation]:
            #print("Match found in matching operation", ass_ua, ass_oa, file=sys.stderr)
            #print(ass_ua in user_attributes, ass_oa in object_attributes, file=sys.stderr)
            if ass_ua in user_attributes and ass_oa in object_attributes:
                return True
        return False
