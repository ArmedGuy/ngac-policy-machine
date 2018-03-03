import json
from flask import Flask, request, jsonify
from ngac.models import Node, NODE_TYPE_U, NODE_TYPE_O, NODE_TYPE_UA, NODE_TYPE_OA
from ngac.policy_machine import PolicyMachine

app = Flask(__name__)



pm = PolicyMachine()

def process_user_policies(parent, level):
    append_id = not parent.id.startswith("pm_")
    for k in level.keys():
        if level[k] == None:
            node = Node(NODE_TYPE_U, (parent.id + "/" if append_id else "") + k, None)
            pm.attach_node(parent, node)
        else:
            node = Node(NODE_TYPE_UA, (parent.id + "/" if append_id else "") + k, None)
            pm.attach_node(parent, node)
            process_user_policies(node, level[k])

def process_object_policies(parent, level):
    append_id = not parent.id.startswith("pm_")
    for k in level.keys():
        if level[k] == None:
            node = Node(NODE_TYPE_O, (parent.id + "/" if append_id else "") + k, None)
            pm.attach_node(parent, node)
        else:
            node = Node(NODE_TYPE_OA, (parent.id + "/" if append_id else "") + k, None)
            pm.attach_node(parent, node)
            process_object_policies(node, level[k])

with open("policy.json", "r") as f:
    policy = json.loads(f.read())
    users = policy['Users']
    objects = policy['Objects']
    process_user_policies(pm.users_node, users)
    process_object_policies(pm.objects_node, objects)
    for assoc in policy['Associations']:
        pm.add_association((assoc['User'], assoc['Operation'], assoc['Object']))


@app.route("/")
def main():
    return 'EHLO'

@app.route("/authorization", methods=["POST"])
def is_authorized():
    req = request.get_json()
    if isinstance(req, list):
        resp = []
        for auth_request in req:
            ua = auth_request['User']
            oa = auth_request['Object']
            operation = auth_request['Operation']
            resp.append({
                "User": ua,
                "Object": oa,
                "Operation": operation,
                "Response": pm.is_allowed(ua, operation, oa)
            })
        return jsonify(resp)
    else:
        auth_request = req
        ua = auth_request['User']
        oa = auth_request['Object']
        operation = auth_request['Operation']
        return jsonify({
            "User": ua,
            "Object": oa,
            "Operation": operation,
            "Response": pm.is_allowed(ua, operation, oa)
        })

if __name__ == '__main__':
    app.run("0.0.0.0", 3000)