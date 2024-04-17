from bson.objectid import ObjectId


class Supervisor:
    @staticmethod
    def _get_mongo():
        from app import mongo
        return mongo

    def __init__(self, first_name, last_name, email=None, phone=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone

        if not self.first_name or not self.last_name:
            raise ValueError("First name and last name are mandatory.")

    def to_dict(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone
        }

    def save(self):
        mongo = self._get_mongo()
        result = mongo.db.supervisors.insert_one(self.to_dict())
        return str(result.inserted_id)

    @staticmethod
    def find_by_id(supervisor_id):
        mongo = Supervisor._get_mongo()
        return mongo.db.supervisors.find_one({'_id': ObjectId(supervisor_id)}, {'_id': 0})

    @staticmethod
    def get_all_supervisors():
        mongo = Supervisor._get_mongo()
        supervisors = list(mongo.db.supervisors.find())

        # Convert ObjectId to string for each supervisor
        for supervisor in supervisors:
            supervisor['_id'] = str(supervisor['_id'])

        return supervisors

    @staticmethod
    def update_supervisor(supervisor_id, update_data):
        mongo = Supervisor._get_mongo()

        # Find the supervisor document by supervisor_id
        supervisor = mongo.db.supervisors.find_one({'_id': ObjectId(supervisor_id)})

        if supervisor:
            # Update the supervisor document with new data
            supervisor.update(**update_data)

            # Save the updated supervisor document
            result = mongo.db.supervisors.replace_one({'_id': ObjectId(supervisor_id)}, supervisor)

            return True
        else:
            # Supervisor not found
            return False

    @staticmethod
    def delete_supervisor(supervisor_id):
        mongo = Supervisor._get_mongo()
        result = mongo.db.supervisors.delete_one({'_id': ObjectId(supervisor_id)})
        return result.deleted_count

