from crypt import methods
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Citizen.sqlite3'
db = SQLAlchemy(app)

class Citizen(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    car = db.Column(db.String(15), default='Possible')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'Citizen {self.name} was registered.'


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        form_content = request.form['content']
        new_citizen = Citizen(name=form_content)

        try:
            db.session.add(new_citizen)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error'

    else:
        citizens = Citizen.query.order_by(Citizen._id).all()
        return render_template('index.html', citizens=citizens)

@app.route('/delete/<int:_id>')
def delete(_id):
    row_to_delete = Citizen.query.get_or_404(_id)

    try:
        db.session.delete(row_to_delete)
        db.session.commit()

        return redirect('/')
    except:
        return 'Error deleting'

@app.route('/update/<int:_id>', methods=['GET', 'POST'])
def update(_id):
    to_update = Citizen.query.get_or_404(_id)

    if request.method == 'POST':
        to_update.name = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Error on update'

    else:
        return render_template('update.html', citizen=to_update)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
