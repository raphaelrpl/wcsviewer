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
                    objs.append(klass(node, **node.attrib))
                    break
        return objs


class SWEList(list):
    def __init__(self, iterable, **attributes):
        super(SWEList, self).__init__(iterable)
        self.attributes = attributes