from flask import Flask
from ngac.models import Node, NODE_TYPE_U, NODE_TYPE_O, NODE_TYPE_UA, NODE_TYPE_OA
from ngac.policy_machine import PolicyMachine

app = Flask(__name__)



pm = PolicyMachine()

pm.users.append(Node(NODE_TYPE_UA, "u1", {
    "Name": "User 1"
}))

@app.route("/")
def main():
    return 'EHLO'

if __name__ == '__main__':
    app.run("0.0.0.0", 3000)