from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Good morning, sunshine!</h1>'


if __name__ == '__main__':
    Flask.run(app, debug=True)
