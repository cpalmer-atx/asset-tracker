from db import db


class AssetModel(db.Model):
    __tablename__ = 'assets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    owner = db.Column(db.String(80))

    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    location = db.relationship('LocationModel')

    def __init__(self, name, owner, location_id):
        self.name = name
        self.owner = owner
        self.location_id = location_id

    def json(self):
        return {'name': self.name, 'owner': self.owner}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()