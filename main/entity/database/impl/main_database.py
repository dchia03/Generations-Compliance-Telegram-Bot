from main.constants.database_names import MAIN_DATABASE_NAME
from main.entity.database.base.database_base import Database
from main.props.properties import PROPS

db = Database(
    mongo_client_str=PROPS.mongo_db_client,
    database_name=MAIN_DATABASE_NAME
)
