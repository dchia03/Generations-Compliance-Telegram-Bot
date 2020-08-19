class ReplyOption(object):
    def __init__(self, name, description=""):
        self.name = name
        if description == "":
            self.description = ""
        else:
            self.description = "{}: {}".format(name, description)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def reply_check(self, msg):
        return msg == self.name
