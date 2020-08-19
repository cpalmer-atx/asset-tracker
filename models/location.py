  
from db import db


class LocationModel(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    assets = db.relationship('AssetModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'assets': [asset.json() for asset in self.assets.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()