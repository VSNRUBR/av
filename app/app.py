from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///register.sqlite3'
db = SQLAlchemy(app)

class Citizen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    car = db.Column(db.String(15), default='Possible')

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
        dummy = Citizen(name='Dummy')
        db.session.add(dummy)
        db.session.commit()

        citizens = Citizen.query.order_by(Citizen.id).all()
        return render_template('index.html', citizens=citizens)




if __name__ == '__main__':
    app.run(debug=True)
