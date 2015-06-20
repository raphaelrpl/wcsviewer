class GMLException(Exception):
    def __init__(self, msg):
        self.msg = msg
        super(GMLException, self).__init__(msg)


class GMLValueError(GMLException):
    pass