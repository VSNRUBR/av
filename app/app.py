import re
from flask import Flask, url_for, render_template, request, redirect, session, flash
from models import db, Citizen, Car

app = Flask(__name__)
app.secret_key = 'A_LONG_SECRET'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.sqlite3'
db.init_app(app)

@app.route('/', methods=['POST', 'GET'])
def index():
    if 'user' in session:
        user = session['user']
        if request.method == 'POST':
            form_content = request.form['content']
            new_citizen = Citizen(name=form_content, sale_op=True)

            try:
                db.session.add(new_citizen)
                db.session.commit()
                return redirect('/')
            except:
                return 'There was an error'

        else:
            citizens = Citizen.query.order_by(Citizen.id).all()
            car_citizen = db.session.query(Citizen.name, db.func.count(Car.citizen_id)) \
                .outerjoin(Car, Citizen.id == Car.citizen_id).group_by(Citizen.name).all()
            car_citizen = dict(car_citizen)
            return render_template('index.html', citizens=citizens, user=user,
                                    car_citizen=car_citizen)
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

@app.route('/delete/<int:id>')
def delete(id):
    row_to_delete = Car.query.get(id)
    citizen_id = row_to_delete.citizen_id

    try:
        db.session.delete(row_to_delete)
        db.session.commit()

        return redirect(url_for('update', id=citizen_id))
    except:
        return 'Error deleting'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    person = Citizen.query.get_or_404(id)
    car_citizen = db.session.query(Citizen.name, Car.id, Car.model, Car.color) \
        .outerjoin(Car, Citizen.id == Car.citizen_id).order_by(Car.id).all()

    list_car_citizen = [tup for tup in car_citizen if tup[0] == person.name]

    if request.method == 'POST':
        if len(list_car_citizen) < 3:
            new_car = Car(citizen=person)
            new_car.color = request.form['colors']
            new_car.model = request.form['models']
            person.sale_opportunity = False

            try:
                db.session.add(new_car)
                db.session.commit()
                return redirect('#')
            except:
                return 'Error on update'
        else:
            flash(f'{person.name.capitalize()} already has 3 cars. Please delete one before adding another.')
            return redirect('#')

    else:
        return render_template('update.html', citizen=person, list_car_citizen=list_car_citizen)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
