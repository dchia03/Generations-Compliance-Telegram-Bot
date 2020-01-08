from main.entity.collection import Collection
from main.entity.document import Document
from main.utils.logger import Logger


class OrderedCollection(Collection):
    def __init__(self, database, collection_name):
        super().__init__(database, collection_name)
        self.log = Logger(__name__)

    def add_document(self, document):
        document.document_obj[Document.DOC_ID_FIELD] = self.get_number_documents()
        return super().add_document(document)

    def get_latest_document(self):
        return self.get_document(
            filter={
                Document.DOC_ID_FIELD: self.get_number_documents() - 1
            }
        )
