from flask import Flask
from services.knight import find_steps_to_target

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def hello_world():
    return 'Welcome to my page!'


@app.route('/about')
def about():
    return '<h1>About</h1>'


# http://localhost:5000/knight/steps/3/4
@app.route('/knight/steps/<int:target_x>/<int:target_y>')
def knight_steps(target_x, target_y):
    steps = find_steps_to_target(target_x, target_y)
    return f'Steps of Knight to target ({target_x}, {target_y}): {steps}'


if __name__ == '__main__':
    app.run()
