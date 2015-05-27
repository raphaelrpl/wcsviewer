class WCSException(Exception):
    def __init__(self, *args, **kwargs):
        super(WCSException, self).__init__(*args, **kwargs)


class WCSInvalidParameter(WCSException):
    def __init__(self, msg="Invalid parameter", value=None, *args, **kwargs):
        self.msg = "%s - \"%s\"" % msg, value
        super(WCSInvalidParameter, self).__init__(*args, **kwargs)


class WCSRequestError(WCSException):
    pass