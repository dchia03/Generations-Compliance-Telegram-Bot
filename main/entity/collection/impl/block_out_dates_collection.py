from main.constants.database_names import BLOCK_OUT_DATES_COLLECTION
from main.entity.collection.base.ordered_collection_base import OrderedCollection
from main.entity.database.impl.main_database import db
from main.entity.document.impl.block_out_dates import BlockOutDates
from main.utils.logger import Logger


class BlockOutDatesCollection(OrderedCollection):
    def __init__(self, database, collection_name):
        super().__init__(database, collection_name)
        self.log = Logger(__name__)

    def get_latest_block_out_dates(self):
        return BlockOutDates(
            block_out_dates_details=self.get_latest_document()
        )

    def add_block_out_dates(self, bod):
        self.add_document(document=bod)


block_out_dates_collection = BlockOutDatesCollection(
    database=db,
    collection_name=BLOCK_OUT_DATES_COLLECTION
)
