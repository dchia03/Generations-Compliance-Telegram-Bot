import datetime as dt

from pytz import timezone

from main.utils.logger import Logger


class Collection(object):
    DOC_DATE_CREATED = "Date Created"
    DOC_DATE_UPDATED = "Date Updated"
    DOC_DATETIME_FIELDS = [DOC_DATE_CREATED, DOC_DATE_UPDATED]
    TIMEZONE = "Singapore"
    DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"
    log = Logger(__name__)

    def __init__(self, database, collection_name):
        self.database = database.get_database()
        self.database_name = database.get_database_name()
        self.collection_name = collection_name
        self.c = self.database[collection_name]

    def get_collection(self):
        return self.c

    def get_collection_list(self):
        return [doc for doc in self.get_collection().find({})]

    def get_number_documents(self):
        return len(self.get_collection_list())

    def get_collection_name(self):
        return self.collection_name

    def get_database(self):
        return self.database

    def add_document(self, document):
        doc = document.get_document()
        time_now = dt.datetime.now(timezone(self.TIMEZONE)).strftime(self.DATETIME_FORMAT)
        for field in self.DOC_DATETIME_FIELDS:
            doc[field] = time_now
        self.get_collection().insert_one(doc)

    def get_document(self, filter):
        res = [doc for doc in self.get_collection().find(filter=filter)]
        if len(res) > 1:
            self.log.info("Multiple Documents Found")
        elif len(res) == 1:
            self.log.info("Single Document Found")
            res = res[0]
        else:
            self.log.info("No Documents Found")
            res = None
        return res

    def update_document(self, updated_document):
        updated_doc = updated_document.get_document()
        updated_doc[self.DOC_DATE_UPDATED] = dt.datetime.now(timezone(self.TIMEZONE)).strftime(self.DATETIME_FORMAT)
        return self.get_collection().find_one_and_update(
            filter={
                updated_document.DOC_ID_FIELD: updated_doc[updated_document.DOC_ID_FIELD]
            },
            update={
                "$set": updated_doc
            }
        )

    def delete_document(self, document):
        return self.get_collection().find_one_and_delete(
            filter={
                document.DOC_ID_FIELD: document.get_datafield(document.DOC_ID_FIELD)
            }
        )
