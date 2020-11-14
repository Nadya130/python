from flask import Flask

app = Flask(__name__)
@app.route('/')
def index():
    return "Hello world"

@app.route('/api/v1/hello-world-4')
def hello_world():
    return 'Hello World 4'


if __name__ == '__main__':
    app.run(debug=True)
