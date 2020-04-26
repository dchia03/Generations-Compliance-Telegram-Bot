import bson

from main.utils.logger import Logger


class Document(object):
    DOC_ID_FIELD = "_id"
    DOC_ID_FIELD_DATA_TYPE = bson.objectid.ObjectId
    log = Logger(__name__)

    def __init__(
            self, all_fields, all_fields_data_type, all_fields_data_format,
            non_editable_fields, document_details=None
    ):
        self.all_fields = all_fields
        self.all_fields_data_type = all_fields_data_type
        self.all_fields_data_format = all_fields_data_format
        self.non_editable_fields = non_editable_fields
        if document_details is None:
            self.document_obj = {field: None for field in self.all_fields}
        else:
            self.document_obj = document_details

    def get_document_id(self):
        return self.document_obj[self.DOC_ID_FIELD]

    def get_document(self):
        return self.document_obj

    def get_all_fields(self):
        return self.all_fields

    def set_datafield(self, field, data):
        if field in self.non_editable_fields:
            self.log.info("Non Editable Field: {}\n".format(field))
            return False
        elif field not in self.document_obj.keys():
            self.log.info("Invalid Field: {}\n".format(field))
            return False
        elif type(data) != self.all_fields_data_type[field]:
            self.log.info("Invalid Data Type: {} ({})".format(data, type(data)))
            self.log.info("Expected Data Type for {}: {}".format(field, self.all_fields_data_type[field]))
            return False
        elif not self.all_fields_data_format[field](data):
            self.log.info("Invalid Data Format: {}\n".format(data))
            return False
        else:
            self.document_obj[field] = data
            return True

    def update_datafield(self, field, data):
        return self.set_datafield(field, data)

    def delete_datafield(self, field):
        if field in self.non_editable_fields:
            self.log.info("Non Editable Field: {}\n".format(field))
            return False
        elif field not in self.document_obj.keys():
            self.log.info("Invalid Field: {}\n".format(field))
            return False
        else:
            self.document_obj[field] = None
            return True

    def get_datafield(self, field):
        if field not in self.document_obj.keys():
            self.log.info("Invalid Field: {}\n".format(field))
            return None
        else:
            return self.document_obj[field]

    def print_document(self):
        msg = ""
        for field in self.all_fields:
            msg += "{}: {}\n".format(field, self.document_obj[field])
        msg += "\n"
        self.log.info(msg)
