from bson.objectid import ObjectId

class FailedDocuments:
    @staticmethod
    def _get_mongo():
        from app import mongo
        return mongo


    def __init__(self, pdf_link):
        self.pdf_link = pdf_link

    def to_dict(self):
        return {
            'pdf_link': self.pdf_link
        }

    def save(self):
        print("################################### DATA")
        print(self.pdf_link)
        mongo = self._get_mongo()
        if mongo is None:
            print("MongoDB client is not initialized.")
            return None

        try:
            result = mongo.db.failed_documents.insert_one(self.to_dict())
            return str(result.inserted_id)
        except Exception as e:
            print(f"Failed to save document: {e}")
            return None

    @staticmethod
    def get_all_failed_documents():
        mongo = FailedDocuments._get_mongo()
        if mongo is None:
            print("MongoDB client is not initialized.")
            return []

        try:
            failed_documents_list = list(mongo.db.failed_documents.find())
            # Convert ObjectId to string for each failed document
            for failed_document in failed_documents_list:
                failed_document['_id'] = str(failed_document['_id'])
            return failed_documents_list
        except Exception as e:
            print(f"Failed to retrieve documents: {e}")
            return []

    @staticmethod
    def delete_failed_document(failed_document_id):
        mongo = FailedDocuments._get_mongo()
        if mongo is None:
            print("MongoDB client is not initialized.")
            return 0

        try:
            result = mongo.db.failed_documents.delete_one({'_id': ObjectId(failed_document_id)})
            return result.deleted_count
        except Exception as e:
            print(f"Failed to delete document: {e}")
            return 0
