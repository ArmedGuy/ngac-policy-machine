from flask import Flask, request, jsonify
from ngac.models import Node, NODE_TYPE_U, NODE_TYPE_O, NODE_TYPE_UA, NODE_TYPE_OA
from ngac.policy_machine import PolicyMachine

app = Flask(__name__)



pm = PolicyMachine()

group1 = Node(NODE_TYPE_UA, "group1", {
    "Name": "Group 1"
})

pm.attach_node(pm.users_node, group1)

user1 = Node(NODE_TYPE_U, "u1", {
    "Name": "User 1"
})

pm.attach_node(group1, user1)

indoor = Node(NODE_TYPE_OA, "indoor", {
    "Name": "Indoor"
})

outdoor = Node(NODE_TYPE_OA, "outdoor", {
    "Name": "Outdoor"
})

temp1 = Node(NODE_TYPE_O, "temp1", {
    "Name": "temp1"
})

temp2 = Node(NODE_TYPE_O, "temp2", {
    "Name": "temp2"
})

pm.attach_node(pm.objects_node, indoor)
pm.attach_node(pm.objects_node, outdoor)
pm.attach_node(indoor, temp1)
pm.attach_node(outdoor, temp2)

pm.add_association((group1, "read", indoor))
pm.add_association((group1, "write", indoor))
pm.add_association((group1, "read", temp2))

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