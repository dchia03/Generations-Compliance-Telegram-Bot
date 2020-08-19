import logging


class Logger(object):
    def __init__(self, class_name):
        logging.basicConfig(
            format="%(asctime)s - %(name)-20s - %(levelname)-8s : %(message)s",
            level=logging.INFO
        )
        self.logger_obj = logging.getLogger(class_name)

    def info(self, msg):
        self.logger_obj.info(msg)

    def warn(self, msg):
        self.logger_obj.warning(msg)

    def debug(self, msg):
        self.logger_obj.debug(msg)

    def error(self, msg):
        self.logger_obj.error(msg)
