from flask_jwt import JWT
from flask_restful import Api
from flask import Flask


# from user import UserRegister
# from asset import Asset, AssetList
from security import authenticate, identity
from resources.asset import Asset, AssetList
from resources.location import Location, LocationList
from resources.user import UserRegister

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True   # Allow flask propagating exception even if debug == False
app.secret_key = 'temp_key'                 # secret key placeholder
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)

api.add_resource(Location, '/location/<string:name>')
api.add_resource(LocationList, '/locations')
api.add_resource(Asset, '/asset/<string:name>')
api.add_resource(AssetList, '/assets')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)