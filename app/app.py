import time
from flask import Flask, render_template, flash, redirect, request, url_for, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt


DBUSER = 'dass'
DBPASS = 'foobarbaz'
DBHOST = 'db'
DBPORT = '5432'
DBNAME = 'userdb'


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=DBUSER,
        passwd=DBPASS,
        host=DBHOST,
        port=DBPORT,
        db=DBNAME)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'foobarbaz'


db = SQLAlchemy(app)



class UserNetflix(db.Model):
    __tablename__ = 'usernetflix'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(50), nullable=False)
    adresse = db.Column(db.String())
    email = db.Column(db.String(120), unique=True)
    pays = db.Column(db.String(120))
    status = db.Column(db.String(120))
    created_at = db.Column(db.DateTime,
                           index=False,
                           nullable=False)

    def __init__(self, nom, adresse, email, pays, status, created_at):
        self.nom = nom
        self.adresse = adresse
        self.email = email
        self.pays = pays
        self.status = status
        self.created_at = created_at

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'adresse': self.adresse,
            'email': self.email,
            'pays': self.pays,
            'status': self.status,
            'created_at': self.created_at

        }

def database_initialization_sequence():
    db.create_all()
    test_rec = UserNetflix(
            'John Doe',
            '123 Foobar Ave',
            'mail@gmail.com',
            'USA',
            'Aticf',
            dt.now()
            )

    db.session.add(test_rec)
    db.session.rollback()
    db.session.commit()

@app.route("/users", methods=['GET'])
def getUsers():
    if request.method == "GET":
        users = UserNetflix.query.all()
        if not users:
            return jsonify([])
        return jsonify([c.serialize() for c in users])

@app.route("/users/add", methods=['POST'])
def addUser():
    if request.method == "POST":
        request_data = request.get_json()
        nom, adresse, email, telephone, pays, status = None, None, None, None, None, None
        print(nom, adresse, email, telephone, pays, status)
        print(request_data)
        if request_data:
            if 'nom' in request_data:
                nom = request_data['nom']
            else:
                return make_response(jsonify({"error": "Attribut nom required"}), 404)

            if 'adresse' in request_data:
                adresse = request_data['adresse']

            if 'email' in request_data:
                email = request_data['email']

            if 'pays' in request_data:
                pays = request_data['pays']

            if 'status' in request_data:
                status = request_data['status']

            find = UserNetflix.query.filter_by(email=email).first()
            if find:
                return jsonify(find.serialize())

            user = UserNetflix(nom=nom, adresse=adresse, email=email, pays=pays, status=status, created_at=dt.now())
            try:
                db.session.add(user)
                db.session.commit()
                return jsonify(user.serialize())
            except AssertionError as e:
                print(str(e))
                return make_response(jsonify({"error": "insertion failed"}), 404)
        return make_response(jsonify({"error": "Data not found"}), 404)

@app.route("/users/<int:user_id>", methods=['GET'])
def client(user_id):
    if request.method == "GET":
        user = UserNetflix.query.get_or_404(user_id)
        return jsonify(user.serialize())

@app.route("/users/edit/<int:user_id>", methods=['PUT'])
def editUser(user_id):
    if request.method == "PUT":
        user = UserNetflix.query.get_or_404(user_id)
        request_data = request.get_json()
        if request_data:
            if 'nom' in request_data:
                nom = request_data['nom']
                user.nom = nom
            else:
                return make_response(jsonify({"error": "Attribut 'nom' required"}), 404)

            if 'adresse' in request_data:
                adresse = request_data['adresse']
                user.adresse = adresse
            if 'email' in request_data:
                email = request_data['email']
                user.email = email

            if 'telephone' in request_data:
                telephone = request_data['telephone']
                user.telephone = telephone

            if 'pays' in request_data:
                pays = request_data['pays']
                user.pays = pays

            if 'status' in request_data:
                status = request_data['status']
                user.status = status
            try:
                db.session.commit()
                return jsonify(user.serialize())
            except AssertionError as e:
                print(str(e))
                return make_response(jsonify({"error": "modification failed"}), 404)
        return make_response(jsonify({"error": "Data not found"}), 404)

@app.route("/users/delete/<int:user_id>", methods=['DELETE'])
def deleteUser(user_id):

    if request.method == "DELETE":
        user = UserNetflix.query.get_or_404(user_id)
        try:
            db.session.delete(user)
            db.session.commit()
        except AssertionError as e:
            print(str(e))
            return make_response(jsonify({"error": "DELETE failed"}), 404)
        return make_response(jsonify({"status": "success"}), 204)

if __name__ == '__main__':
    print("beginng")
    dbstatus = False
    while dbstatus == False:
        print("in while")
        try:
            db.create_all()
        except:
            print("sleep 1")
            time.sleep(1)
        else:
            dbstatus = True
            print("statusDB 1")
    database_initialization_sequence()
    print("init db")
    app.run(debug=True, host='0.0.0.0')
