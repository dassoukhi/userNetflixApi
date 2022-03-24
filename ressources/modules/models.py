from app import db

assert isinstance(db.Model, object)

class UserNetflix(db.Model):
    __tablename__ = 'usernetflix'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(50), nullable=False)
    adresse = db.Column(db.String())
    email = db.Column(db.String(120), unique=True)
    pays = db.Column(db.String(120), unique=True)
    status = db.Column(db.String(120), unique=True)
    created_at = db.Column(db.DateTime,
                           index=False,
                           unique=False,
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