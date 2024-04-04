from bson.objectid import ObjectId

class User:
    @staticmethod
    def _get_mongo():
        from app import mongo
        return mongo

    def __init__(self, cohort=None, title=None, first_name=None, last_name=None, rsa_id_number=None, mobile_number=None, email=None, gender=None, race=None, disabled=None, residential_address=None, tax_number=None, bank_account_number=None, bank_account_type=None, bank_branch_code=None, next_of_kin_name=None, next_of_kin_relationship=None, next_of_kin_mobile_no=None, supervisor=None, host_name=None, host_site=None, employee_contract_signed=None, work_experience_title=None, monthly_salary=None, start_date=None, end_date=None, isValidated = False, files = []):
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
        self.supervisor = supervisor
        self.host_name = host_name
        self.host_site = host_site
        self.employee_contract_signed = employee_contract_signed
        self.work_experience_title = work_experience_title
        self.monthly_salary = monthly_salary
        self.start_date = start_date
        self.end_date = end_date
        self.isValidated = isValidated
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
