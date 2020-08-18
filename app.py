from flask import Flask
from flask_restful import Resource, Api

from resources.asset import *
from resources.location import *

app = Flask(__name__)
api = Api(app)

if __name__ == '__main__':
    app.run(port=5000, debug=True)