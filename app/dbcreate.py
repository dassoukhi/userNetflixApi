from app import db, UserNetflix
from datetime import datetime as dt

db.create_all()


test_rec = UserNetflix(
            'John Doe',
            '123 Foobar Ave',
            'Los Angeles',
            'mail@gmail.com',
            'USA',
            'Aticf',
            dt.now()
            )


db.session.add(test_rec)
db.session.commit()
