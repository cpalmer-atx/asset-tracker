from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3


class Asset(Resource):
    TABLE_NAME = 'assets'

    parser = reqparse.RequestParser()
    parser.add_argument('owner',
        required=True,
        help="Assets must have an owner!"
    )

    @jwt_required()
    def get(self, name):
        asset = self.find_by_name(name)
        if asset:
            return asset
        return {'message': 'Asset not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE name=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'asset': {'name': row[0], 'owner': row[1]}}

    def post(self, name):
        if self.find_by_name(name):
            return {'message': "An asset named '{}' already exists.".format(name)}

        data = Asset.parser.parse_args()

        asset = {'name': name, 'owner': data['owner']}

        try:
            Asset.insert(asset)
        except:
            return {"message": "An error occurred inserting the asset."}

        return asset

    @classmethod
    def insert(cls, asset):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO {table} VALUES(?, ?)".format(table=cls.TABLE_NAME)
        cursor.execute(query, (asset['name'], asset['owner']))

        connection.commit()
        connection.close()

    @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM {table} WHERE name=?".format(table=self.TABLE_NAME)
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Asset deleted'}

    @jwt_required()
    def put(self, name):
        data = Asset.parser.parse_args()
        asset = self.find_by_name(name)
        updated_asset = {'name': name, 'owner': data['owner']}
        if asset is None:
            try:
                Asset.insert(updated_asset)
            except:
                return {"message": "An error occurred inserting the asset."}
        else:
            try:
                Asset.update(updated_asset)
            except:
                return {"message": "An error occurred updating the asset."}
        return updated_asset

    @classmethod
    def update(cls, asset):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE {table} SET owner=? WHERE name=?".format(table=cls.TABLE_NAME)
        cursor.execute(query, (asset['owner'], asset['name']))

        connection.commit()
        connection.close()


class AssetList(Resource):
    TABLE_NAME = 'assets'

    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table}".format(table=self.TABLE_NAME)
        result = cursor.execute(query)
        assets = []
        for row in result:
            assets.append({'name': row[0], 'owner': row[1]})
        connection.close()

        return {'assets': assets}