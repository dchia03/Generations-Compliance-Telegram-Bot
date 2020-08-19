import unittest

from bson.objectid import ObjectId

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
        self.assertIsNotNone(self.doc.get_document())

    def test_get_all_fields(self):
        self.log.info(self.info_msg_base + "test_get_all_fields")
        self.assertEqual(sorted(self.doc.get_all_fields()), ["field 1"])

    def test_datafield_operations(self):
        self.log.info(self.info_msg_base + "test_datafield_operations")
        self.assertFalse(self.doc.set_datafield("field 2", "value 1"))
        self.assertFalse(self.doc.set_datafield("field 1", 1))
        self.assertTrue(self.doc.set_datafield("field 1", "value 1"))

        self.assertEqual(self.doc.get_datafield("field 1"), "value 1")
        self.assertIsNone(self.doc.get_datafield("field 2"))

        self.assertFalse(self.doc.update_datafield("field 2", "value 1"))
        self.assertFalse(self.doc.update_datafield("field 1", 1))
        self.assertTrue(self.doc.update_datafield("field 1", "value 2"))
        self.assertEqual(self.doc.get_datafield("field 1"), "value 2")

        self.assertFalse(self.doc.delete_datafield("field 2"))
        self.doc.print_document()
        self.assertTrue(self.doc.delete_datafield("field 1"))
        self.doc.print_document()

    def test_init_with_document_details(self):
        doc = Document(
            all_fields=["a"],
            all_fields_data_type={"a": str},
            all_fields_data_format={"field 1": lambda value: isinstance(value, str)},
            document_details={"a": "test", Document.DOC_ID_FIELD: ObjectId()}
        )
        self.assertEqual(doc.get_datafield("a"), "test")
        doc.print_document()
        self.log.info("Document id: " + str(doc.get_document_id()))
        self.assertFalse(doc.set_datafield(Document.DOC_ID_FIELD, ObjectId()))
        self.assertFalse(doc.delete_datafield(Document.DOC_ID_FIELD))
