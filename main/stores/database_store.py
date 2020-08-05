###############
## Databases ##
###############
########
# Keys #
########

from main.constants.database import *
from main.entity.collection import Collection
from main.entity.database import Database
from main.entity.ordered_collection import OrderedCollection
from main.utils.properties import Properties

props = Properties()

##################
# Admin Database #
##################

db = Database(
    mongo_client_str=props.mongo_db_client,
    database_name=MAIN_DATABASE_NAME
)

admin_db = Collection(
    database=db,
    collection_name=ADMINISTRATION_COLLECTION
)

###################
# Roster Database #
###################

roster_db = OrderedCollection(
    database=db,
    collection_name=ROSTER_COLLECTION
)

##########################
# BlockOutDates Database #
##########################

block_out_dates_db = OrderedCollection(
    database=db,
    collection_name=BLOCK_OUT_DATES_COLLECTION
)

##########################
# BlockOutDates Database #
##########################

duty_management_db = Collection(
    database=db,
    collection_name=DUTY_MANAGEMENT_COLLECTION
)
