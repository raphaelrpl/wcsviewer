from libs.pyogc.ogc.gml.exceptions import GMLValueError

class GMLBase(object):
    def __init__(self, **attributes):
        self.attributes = attributes


class GMLRangeBase(GMLBase):
    def __init__(self, limits):
        attrs = {}
        if isinstance(limits, dict):
            attrs.update(limits.get('attributes', {}) or limits.get('attrs', {}))
            limits = limits.get('values')

        super(GMLRangeBase, self).__init__(**attrs)

        if isinstance(limits, basestring):
            self.limits = limits.split(' ')
        elif isinstance(limits, list) or isinstance(limits, tuple) or isinstance(limits, set):
            self.limits = limits
        else:
            raise GMLValueError("Invalid type of limits. Expected a string or iterable. Got {0}".format(limits))