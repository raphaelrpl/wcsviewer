from libs.pyogc.ogc.gml.exceptions import GMLValueError
import re

class GMLBase(object):
    xml_tag = ""

    def __init__(self, **attributes):
        self.attributes = attributes

    @classmethod
    def format_attr(cls, attr):
        validator = re.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')
        return validator.sub(r'_\1', attr).lower()

    @classmethod
    def initialize_elements(cls, element):
        objs = []
        for node in element:
            namespace = "{%s}" % node.nsmap['gml']
            for klass in type.__subclasses__(GMLBase):
                if namespace + klass.xml_tag == node.tag:
                    # initialize class
                    objs.append(klass(node, **node.attrib))
        return objs


class GMLRangeBase(GMLBase, list):
    def __init__(self, limits):
        attrs = {}
        if isinstance(limits, dict):
            attrs.update(limits.get('attributes', {}) or limits.get('attrs', {}))
            limits = limits.get('values', "").split(' ')
        elif hasattr(limits, 'getchildren'):
            # node element
            attrs.update(limits.attrib)
            limits = limits.text

        if isinstance(limits, basestring):
            self.limits = limits.split(' ')
        elif isinstance(limits, list) or isinstance(limits, tuple) or isinstance(limits, set):
            self.limits = limits
        else:
            raise GMLValueError("Invalid type of limits. Expected a string or iterable. Got {0}".format(limits))
        GMLBase.__init__(self, **attrs)
        list.__init__(self, self.limits)

        # super(GMLRangeBase, self).__init__(**attrs)