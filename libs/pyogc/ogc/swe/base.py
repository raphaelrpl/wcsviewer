class SWEBase(object):
    xml_tag = ""

    def __init__(self, **attributes):
        self.attributes = attributes

    @classmethod
    def initialize_elements(cls, element):
        objs = []
        for node in element:
            namespace = "{%s}" % node.nsmap['swe']
            for klass in type.__subclasses__(SWEBase):
                if namespace + klass.xml_tag == node.tag:
                    # initialize class
                    objs.append(klass(node, **node.attrib))
        return objs


class SWEList(SWEBase, list):
    def __init__(self, iterable, **attributes):
        SWEBase.__init__(self, **attributes)
        list.__init__(self, iterable)
        self.attributes = attributes