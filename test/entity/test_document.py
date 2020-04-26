import unittest

from main.entity.document import Document
from main.utils.logger import Logger


class TestDocument(unittest.TestCase):
    def setUp(self):
        self.log = Logger(__name__)
        self.info_msg_base = "Testing {}: ".format(__name__)
        self.doc = Document(
            all_fields=["field 1"],
            all_fields_data_type={"field 1": str},
            all_fields_data_format={"field 1": lambda value: isinstance(value, str)},
            non_editable_fields=[]
        )

    def test_get_document(self):
        self.log.info(self.info_msg_base + "test_get_document")
        assert(self.doc.get_document() is not None)

    def test_get_all_fields(self):
        self.log.info(self.info_msg_base + "test_get_all_fields")
        assert(sorted(self.doc.get_all_fields()) == ["field 1"])

    def test_datafield_operations(self):
        self.log.info(self.info_msg_base + "test_datafield_operations")
        assert(not self.doc.set_datafield("field 2", "value 1"))
        assert(not self.doc.set_datafield("field 1", 1))
        assert(self.doc.set_datafield("field 1", "value 1"))

        assert(self.doc.get_datafield("field 1") == "value 1")
        assert(self.doc.get_datafield("field 2") is None)

        assert(not self.doc.update_datafield("field 2", "value 1"))
        assert(not self.doc.update_datafield("field 1", 1))
        assert(self.doc.update_datafield("field 1", "value 2"))
        assert(self.doc.get_datafield("field 1") == "value 2")

        assert(not self.doc.delete_datafield("field 2"))
        self.doc.print_document()
        assert(self.doc.delete_datafield("field 1"))
        self.doc.print_document()

