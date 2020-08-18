from flask_jwt import JWT, jwt_required, current_identity
from flask_restful import Resource, Api, reqparse
from flask import Flask, request

from security import authenticate, identity
# from resources.asset import *
# from resources.location import *

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True   # Allow flask propagating exception even if debug == False
app.secret_key = 'temp_key'                 # secret key placeholder
api = Api(app)
jwt = JWT(app, authenticate, identity)
assets = []

class Asset(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('owner',
        required=True,
        help="Assets must have an owner!"
    )

    @jwt_required()
    def get(self, name):
        return {'asset': next(filter(lambda x: x['name'] == name, assets), None)}

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, assets), None) is not None:
            return {'message': "An asset named '{}' already exists.".format(name)}
        data = Asset.parser.parse_args()
        asset = {'name': name, 'owner': data['owner']}
        assets.append(asset)
        return asset

    @jwt_required()
    def delete(self, name):
        global assets
        assets = list(filter(lambda x: x['name'] != name, assets))
        return {'message': 'Asset deleted'}

    @jwt_required()
    def put(self, name):
        data = Asset.parser.parse_args()
        asset = next(filter(lambda x: x['name'] == name, assets), None)
        if asset is None:
            asset = {'name': name, 'owner': data['owner']}
            assets.append(asset)
        else:
            asset.update(data)
        return asset

class AssetList(Resource):
    def get(self):
        return {'assets': assets}

api.add_resource(Asset, '/asset/<string:name>')
api.add_resource(AssetList, '/assets')

if __name__ == '__main__':
    app.run(port=5000, debug=True)