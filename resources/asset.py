from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.asset import AssetModel


class Asset(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('owner',
                        required=True,
                        help="Assets must have an owner!"
                        )
    parser.add_argument('location_id',
                        type=int,
                        required=True,
                        help="Every location needs a location_id."
                        )

    @jwt_required()
    def get(self, name):
        asset = AssetModel.find_by_name(name)
        if asset:
            return asset.json()
        return {'message': 'Asset not found'}, 404

    def post(self, name):
        if AssetModel.find_by_name(name):
            return {'message': "An asset named '{}' already exists.".format(name)}, 400

        data = Asset.parser.parse_args()

        asset = AssetModel(name, **data)

        try:
            asset.save_to_db()
        except:
            return {"message": "An error occurred inserting the asset."}, 500

        return asset.json(), 201

    def delete(self, name):
        asset = AssetModel.find_by_name(name)
        if asset:
            asset.delete_from_db()
            return {'message': 'Asset deleted.'}
        return {'message': 'Asset not found.'}, 404

    def put(self, name):
        data = Asset.parser.parse_args()

        asset = AssetModel.find_by_name(name)

        if asset:
            asset.owner = data['owner']
        else:
            asset = AssetModel(name, **data)

        asset.save_to_db()

        return asset.json()


class AssetList(Resource):
    def get(self):
        return {'assets': list(map(lambda x: x.json(), AssetModel.query.all()))}