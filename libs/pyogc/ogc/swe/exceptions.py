class SWEException(Exception):
    def __init__(self, msg):
        self.msg = msg
        super(SWEException, self).__init__(msg)


class SWEValueError(SWEException):
    pass