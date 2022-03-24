from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
import click
from flask.cli import with_appcontext
from flask_migrate import Migrate
from datetime import datetime as dt

load_dotenv()
# This is a sample Python script.


# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['DEBUG'] = True
app.secret_key = os.environ['SECRET_KEY']
app.config["CORS_HEADERS"] = "Content-Type"
db = SQLAlchemy(app)


@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()
    print("create")


app.cli.add_command(create_tables)

migrate = Migrate(app, db)
from ressources.modules.models import *


@app.teardown_request
def checkin_db(exc):
    try:
        print("Removing db session.")
        db.session.remove()
    except AttributeError:
        pass


@app.route("/")
def print_hi():
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, dass')  # Press Ctrl+F8 to toggle the breakpoint.
    return "Hello Dass"


# Press the green button in the gutter to run the script.

@app.route("/users", methods=['GET'])
def getUsers():
    if request.method == "GET":
        users = UserNetflix.query.all()
        print("count:", len(users))
        if not users:
            return {}
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
    app.run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
