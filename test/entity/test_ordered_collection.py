import unittest

import properties as props
from main.entity.database import Database
from main.entity.ordered_collection import OrderedCollection
from main.entity.document import Document
from main.utils.logger import Logger
from properties import Properties


class TestOrderedCollection(unittest.TestCase):
    def setUp(self):
        self.log = Logger(__name__)
        self.info_msg_base = "Testing {}: ".format(__name__)
        self.props = Properties("TEST")
        self.ordered_collection = OrderedCollection(
            Database(self.props.mongo_client_str, "test"),
            "test"
        )

    def test_ordered_collection_functions(self):
        self.log.info(self.info_msg_base + "test_ordered_collection_functions")
        doc = Document(
            all_fields=["field 1"],
            all_fields_data_type={"field 1": str},
            all_fields_data_format={"field 1": lambda value: isinstance(value, str)},
            non_editable_fields=[]
        )
        doc.set_datafield("field 1", "value 1")
        self.ordered_collection.add_document(doc)
        res = self.ordered_collection.get_latest_document()
        self.log.info(res)
        assert(isinstance(res, dict))

        retrieved_doc = Document(
            all_fields=["field 1"],
            all_fields_data_type={"field 1": str},
            all_fields_data_format={"field 1": lambda value: isinstance(value, str)},
            non_editable_fields=[],
            document_details=res
        )
        self.ordered_collection.delete_document(retrieved_doc)
