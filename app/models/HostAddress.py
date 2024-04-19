from bson.objectid import ObjectId

class HostAddress:
    @staticmethod
    def _get_mongo():
        from app import mongo
        return mongo

    def __init__(self, host, host_address):
        self.host = host
        self.host_address = host_address

        if not self.host_address:
            raise ValueError("Host address is mandatory.")

    def to_dict(self):
        return {
            'host': self.host,
            'host_address': self.host_address
        }

    def save(self):
        mongo = self._get_mongo()
        result = mongo.db.host_addresses.insert_one(self.to_dict())
        return str(result.inserted_id)

    @staticmethod
    def find_by_id(address_id):
        mongo = HostAddress._get_mongo()
        return mongo.db.host_addresses.find_one({'_id': ObjectId(address_id)}, {'_id': 0})

    @staticmethod
    def get_all_addresses():
        mongo = HostAddress._get_mongo()
        addresses = list(mongo.db.host_addresses.find())

        # Convert ObjectId to string for each address
        for address in addresses:
            address['_id'] = str(address['_id'])

        return addresses

    @staticmethod
    def update_address(address_id, update_data):
        mongo = HostAddress._get_mongo()

        # Find the address document by address_id
        address = mongo.db.host_addresses.find_one({'_id': ObjectId(address_id)})

        if address:
            # Update the address document with new data
            address.update(**update_data)

            # Save the updated address document
            result = mongo.db.host_addresses.replace_one({'_id': ObjectId(address_id)}, address)

            return True
        else:
            # Address not found
            return False

    @staticmethod
    def delete_address(address_id):
        mongo = HostAddress._get_mongo()
        result = mongo.db.host_addresses.delete_one({'_id': ObjectId(address_id)})
        return result.deleted_count

    @staticmethod
    def create_unique_index():
        mongo = HostAddress._get_mongo()
        mongo.db.host_addresses.create_index([('host_address', 1)], unique=True)
