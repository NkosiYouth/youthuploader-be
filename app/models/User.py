from bson.objectid import ObjectId

class User:
    @staticmethod
    def _get_mongo():
        from app import mongo
        return mongo

    def __init__(self, cohort=None, title=None, first_name=None, last_name=None, rsa_id_number=None, mobile_number=None, email=None, gender=None, race=None, disabled=None, residential_address=None, host_name=None, host_site=None, tax_number=None, bank_account_number=None, bank_account_type=None, bank_branch_code=None, next_of_kin_name=None, next_of_kin_relationship=None, next_of_kin_mobile_no=None, supervisor=None, host=None, host_address=None, employee_contract_signed=None, work_experience_title=None, monthly_salary=None, start_date=None, end_date=None, isValidated = False, isUpdated = False, files = []):
        self.cohort = cohort
        self.title = title
        self.first_name = first_name
        self.last_name = last_name
        self.rsa_id_number = rsa_id_number
        self.mobile_number = mobile_number
        self.email = email
        self.gender = gender
        self.race = race
        self.disabled = disabled
        self.residential_address = residential_address
        self.tax_number = tax_number
        self.bank_account_number = bank_account_number
        self.bank_account_type = bank_account_type
        self.bank_branch_code = bank_branch_code
        self.next_of_kin_name = next_of_kin_name
        self.next_of_kin_relationship = next_of_kin_relationship
        self.next_of_kin_mobile_no = next_of_kin_mobile_no
        self.host_name = host_name
        self.host_site = host_site
        # self.supervisor = supervisor
        # self.host = host
        # self.supervisor = ObjectId(supervisor) if supervisor else None
        self.supervisor = ObjectId(supervisor) if isinstance(supervisor, str) else supervisor if supervisor else None
        self.host = ObjectId(host) if host else None
        self.host_address = ObjectId(host_address) if host else None
        self.employee_contract_signed = employee_contract_signed
        self.work_experience_title = work_experience_title
        self.monthly_salary = monthly_salary
        self.start_date = start_date
        self.end_date = end_date
        self.isValidated = isValidated
        self.isUpdated = isUpdated
        self.files = files

    def to_dict(self):
        user_dict = {}
        for attr, value in self.__dict__.items():
            if value is not None:
                user_dict[attr] = value
        return user_dict

    def save(self):
        mongo = self._get_mongo()
        result = mongo.db.users.insert_one(self.to_dict())
        return str(result.inserted_id)

    @staticmethod
    def find_by_id(user_id):
        mongo = User._get_mongo()
        return mongo.db.users.find_one({'_id': ObjectId(user_id)}, {'_id': 0})

    @staticmethod
    def get_all_users(params=None):
        mongo = User._get_mongo()
        query = {}  # Initialize an empty query
        print(params)
        if params:
            query.update(params)  # Update query with provided parameters
            if 'isValidated' in params:
                query['isValidated'] = params['isValidated'] == 'true'


        users = list(mongo.db.users.find(query))

        # Convert ObjectId to string for each user
        for user in users:
            user['_id'] = str(user['_id'])

        return users


    @staticmethod
    def update_user(user_id, update_data):
        mongo = User._get_mongo()

        # Find the user document by user_id
        user = mongo.db.users.find_one({'_id': ObjectId(user_id)})

        if user:
            # Update the user document with new data
            user.update(**update_data)

            # Save the updated user document
            result = mongo.db.users.replace_one({'_id': ObjectId(user_id)}, user)

            return True
        else:
            # User not found
            return False

    @staticmethod
    def delete_user(user_id):
        mongo = User._get_mongo()
        result = mongo.db.users.delete_one({'_id': ObjectId(user_id)})
        return result.deleted_count


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


class Host:
    @staticmethod
    def _get_mongo():
        from app import mongo
        return mongo

    def __init__(self, host_name, host_site_address):
        self.host_name = host_name
        self.host_site_address = host_site_address

        if not self.host_name:
            raise ValueError("Host name is mandatory.")

    def to_dict(self):
        return {
            'host_name': self.host_name,
            'host_site_address': self.host_site_address
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
