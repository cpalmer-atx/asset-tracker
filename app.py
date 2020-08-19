from flask_jwt import JWT, jwt_required, current_identity
from flask_restful import Resource, Api, reqparse
from flask import Flask, request

from security import authenticate, identity
from user import UserRegister
from asset import Asset, AssetList
# from resources.asset import *
# from resources.location import *

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True   # Allow flask propagating exception even if debug == False
app.secret_key = 'temp_key'                 # secret key placeholder
api = Api(app)
jwt = JWT(app, authenticate, identity)

api.add_resource(Asset, '/asset/<string:name>')
api.add_resource(AssetList, '/assets')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(port=5000, debug=True)