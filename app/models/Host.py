from bson.objectid import ObjectId

class Host:
    @staticmethod
    def _get_mongo():
        from app import mongo
        return mongo

    def __init__(self, host_name):
        self.host_name = host_name

        if not self.host_name:
            raise ValueError("Host name is mandatory.")

    def to_dict(self):
        return {
            'host_name': self.host_name,
        }

    def save(self):
        mongo = self._get_mongo()
        result = mongo.db.hosts.insert_one(self.to_dict())
        return str(result.inserted_id)

    @staticmethod
    def find_by_id(host_id):
        mongo = Host._get_mongo()
        return mongo.db.hosts.find_one({'_id': ObjectId(host_id)}, {'_id': 0})

    @staticmethod
    def get_all_hosts():
        mongo = Host._get_mongo()
        hosts = list(mongo.db.hosts.find())

        # Convert ObjectId to string for each host
        for host in hosts:
            host['_id'] = str(host['_id'])

        return hosts

    @staticmethod
    def update_host(host_id, update_data):
        mongo = Host._get_mongo()

        # Find the host document by host_id
        host = mongo.db.hosts.find_one({'_id': ObjectId(host_id)})

        if host:
            # Update the host document with new data
            host.update(**update_data)

            # Save the updated host document
            result = mongo.db.hosts.replace_one({'_id': ObjectId(host_id)}, host)

            return True
        else:
            # Host not found
            return False

    @staticmethod
    def delete_host(host_id):
        mongo = Host._get_mongo()
        result = mongo.db.hosts.delete_one({'_id': ObjectId(host_id)})
        return result.deleted_count

    @staticmethod
    def create_unique_index():
        mongo = Host._get_mongo()
        mongo.db.hosts.create_index([('host_name', 1)], unique=True)
