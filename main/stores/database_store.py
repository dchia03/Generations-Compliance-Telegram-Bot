###############
## Databases ##
###############
########
# Keys #
########
import sys

from main.entity.collection import Collection
from main.entity.database import Database
from main.entity.ordered_collection import OrderedCollection
from properties import props

##################
# Admin Database #
##################

db = Database(
    mongo_client_str=props.mongo_client_str,
    database_name="GenerationsCompliance"
)

admin_db = Collection(
    database=db,
    collection_name="AdministrationList"
)

###################
# Roster Database #
###################

roster_db = OrderedCollection(
    database=db,
    collection_name="Roster"
)

##########################
# BlockOutDates Database #
##########################

block_out_dates_db = OrderedCollection(
    database=db,
    collection_name="BlockOutDates"
)

##########################
# BlockOutDates Database #
##########################

duty_management_db = Collection(
    database=db,
    collection_name="DutyManagement"
)
