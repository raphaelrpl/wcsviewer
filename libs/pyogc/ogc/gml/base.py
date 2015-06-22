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
        gml_elements = element.xpath('//gml:*', namespaces={"gml": "http://www.opengis.net/gml/3.2"})

        gml_list = []

        base_classes_list = type.__subclasses__(GMLBase) + type.__subclasses__(GMLRangeBase)

        for elm in gml_elements:
            namespace = "{%s}" % elm.nsmap['gml']
            for klass in base_classes_list:
                if namespace + klass.xml_tag == elm.tag:
                    # initialize class
                    gml_list.append(klass(elm, **elm.attrib))
                    break

        for obj in gml_list:
            print(obj)

        for node in element:
            namespace = "{%s}" % node.nsmap['gml']
            for klass in type.__subclasses__(GMLBase):
                if namespace + klass.xml_tag == node.tag:
                    # initialize class
                    objs.append(klass(node, **node.attrib))
        return objs


class GMLRangeBase(list):
    def __init__(self, limits):
        attrs = {}
        if isinstance(limits, dict):
            attrs.update(limits.get('attributes', {}) or limits.get('attrs', {}))
            limits = limits.get('values', "").split(' ')
        elif hasattr(limits, 'getchildren'):
            # node element
            self.element = limits
            attrs.update(limits.attrib)
            limits = limits.text

        if isinstance(limits, basestring):
            limits = limits.split(' ')
        elif isinstance(limits, list) or isinstance(limits, tuple) or isinstance(limits, set):
            limits = limits
        else:
            raise GMLValueError("Invalid type of limits. Expected a string or iterable. Got {0}".format(limits))
        super(GMLRangeBase, self).__init__(limits)
        # GMLBase.__init__(self, **attrs)

        # super(GMLRangeBase, self).__init__(**attrs)