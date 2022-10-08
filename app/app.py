from flask import Flask, url_for, render_template, request, redirect, session
from models import db, Citizen

app = Flask(__name__)
app.secret_key = 'A_LONG_SECRET'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Citizen.sqlite3'
db.init_app(app)

@app.route('/', methods=['POST', 'GET'])
def index():
    if 'user' in session:
        user = session['user']
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
            return render_template('index.html', citizens=citizens, user=user)
    else:
        return redirect(url_for('login'))

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['email']
        session['user'] = user
        return redirect('/')
    else:
        if 'user' in session:
            return redirect('/')

        return render_template('login.html')

@app.route('/logout/')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

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
