from flask import Flask
from wsgiref.simple_server import make_server
app = Flask(__name__)

@app.route('/api/v1/hello-world-4')
def hello_world():
    return 'Hello, World 4!'

with make_server('',5000,app)as server:
    print("Port 127.0.0.1:5000")

    server.serve_forever()

    #http://127.0.0.1:5000/api/v1/hello-world-4