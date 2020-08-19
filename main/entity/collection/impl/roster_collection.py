from main.constants.database_names import ROSTER_COLLECTION
from main.entity.collection.base.ordered_collection_base import OrderedCollection
from main.entity.database.impl.main_database import db
from main.entity.document.impl.roster import Roster
from main.utils.logger import Logger


class RosterCollection(OrderedCollection):
    def __init__(self, database, collection_name):
        super().__init__(database, collection_name)
        self.log = Logger(__name__)

    def get_latest_roster(self):
        return Roster(roster_details=self.get_latest_document())

    def add_roster(self, roster):
        self.add_document(roster)


roster_collection = RosterCollection(
    database=db,
    collection_name=ROSTER_COLLECTION
)
