from flask_restful import Resource
from models.location import LocationModel


class Location(Resource):
    def get(self, name):
        location = LocationModel.find_by_name(name)
        if location:
            return location.json()
        return {'message': 'Location not found'}, 404

    def post(self, name):
        if LocationModel.find_by_name(name):
            return {'message': "A location named '{}' already exists.".format(name)}, 400

        location = LocationModel(name)
        try:
            location.save_to_db()
        except:
            return {"message": "An error occurred creating the location."}, 500

        return location.json(), 201

    def delete(self, name):
        location = LocationModel.find_by_name(name)
        if location:
            location.delete_from_db()

        return {'message': 'Location deleted'}


class LocationList(Resource):
    def get(self):
        return {'locations': list(map(lambda x: x.json(), LocationModel.query.all()))}