from bson.objectid import ObjectId

class RawData:
    @staticmethod
    def _get_mongo():
        from app import mongo
        return mongo

    def __init__(self, user_id, elements, file_name):
        self.user_id = user_id
        self.elements = elements
        self.file_name = file_name

    def to_dict(self):
        return {
            'user_id': ObjectId(self.user_id),  # Convert user_id to ObjectId
            'file_name': self.file_name,
            'elements': self.elements
        }

    def save(self):
        mongo = self._get_mongo()
        result = mongo.db.raw_data.insert_one(self.to_dict())
        return str(result.inserted_id)

    @staticmethod
    def find_by_user_id(user_id):
        mongo = RawData._get_mongo()
        return mongo.db.raw_data.find_one({'user_id': ObjectId(user_id)}, {'_id': 0})

    @staticmethod
    def get_all_raw_data():
        mongo = RawData._get_mongo()
        raw_data_list = list(mongo.db.raw_data.find())

        # Convert ObjectId to string for each raw data
        for raw_data in raw_data_list:
            mongo = RawData._get_mongo()
            raw_data['_id'] = str(raw_data['_id'])

        return raw_data_list

    @staticmethod
    def update_raw_data(raw_data_id, update_data):
        mongo = RawData._get_mongo()
        result = mongo.db.raw_data.update_one({'_id': ObjectId(raw_data_id)}, {'$set': update_data})
        return result.modified_count > 0

    @staticmethod
    def delete_raw_data(raw_data_id):
        mongo = RawData._get_mongo()
        result = mongo.db.raw_data.delete_one({'_id': ObjectId(raw_data_id)})
        return result.deleted_count
