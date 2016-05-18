#!../bin/python
import ConfigParser

from flask import Flask, jsonify

configFile = "/home4/healem/keys/wbtn.cnf"
app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': 'Buy groceries',
        'description': 'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': 'Learn Python',
        'description': 'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.route('/')
def hello_world():
    return "Hello World!"

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

config = ConfigParser.ConfigParser()
config.read(configFile)
readPw = config.get("db", "healem_read")

if __name__ == '__main__':
    app.run(debug=True)

