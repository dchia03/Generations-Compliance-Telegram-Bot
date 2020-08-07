import argparse
import json
import os

from main.utils.logger import Logger

FILE_FORMAT = ".json"
CHATBOT_TOKEN_FIELD = "chatbot_token"
MONGO_DB_CLIENT_FIELD = "mongo_db_client"
VALID_ENVIRONMENTS = ["DEV", "PRD"]


class Properties(object):

    def __init__(self):
        self.log = Logger(__name__)
        self.parser = argparse.ArgumentParser(
            description="Retrieving Properties"
        )
        self.parser.add_argument(
            "-f",
            help="Enter Properties Filename (.json file)", type=str,
            dest="filename"
        )
        self.parser.add_argument(
            "-env", default="DEV", choices=VALID_ENVIRONMENTS,
            help="Enter Environment to run in (default: DEV)", type=str,
            dest="environment"
        )
        self.parser.add_argument(
            "-p", default=os.getcwd(),
            help="Enter Project Path Directory", type=str,
            dest="project_path"
        )
        self.log.info("Current Working Directory: " + os.getcwd())
        self.properties, self.environment = self.get_properties_and_environment()
        self.chatbot_token = self.properties[CHATBOT_TOKEN_FIELD]
        self.mongo_db_client = self.properties[MONGO_DB_CLIENT_FIELD]

    def get_properties_and_environment(self):
        args = self.parser.parse_args()
        filename = args.filename
        environment = args.environment.upper()
        project_path = args.project_path
        self.log.info("Extracting properties from: " + environment)
        self.log.info("Project Path: " + project_path)
        if FILE_FORMAT not in filename:
            self.log.info("Adding file extension to filename: " + filename)
            filename += FILE_FORMAT

        with open(os.path.join(project_path, filename), 'r') as f:
            props_dict = json.load(f)
        environment_properties = props_dict[environment.upper()]
        if environment_properties is None:
            self.log.error("Properties not found for Environment: " + environment)
        return environment_properties, environment
