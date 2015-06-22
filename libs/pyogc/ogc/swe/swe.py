from libs.pyogc.ogc.swe.base import SWEBase, SWEList


class SWEField(SWEBase):
    xml_tag = "field"


class SWEQuantity(SWEBase):
    xml_tag = "Quantity"
    description = ""
    uom = ""


class SWEInterval(SWEList):
    xml_tag = "interval"

    def __init__(self, data):
        attribs = {}
        iterable = None
        if hasattr(data, 'getparent'):
            attribs.update(data.attrib)
            iterable = data.text.split(' ')
        if isinstance(data, basestring) or isinstance(data, list):
            iterable = data
        super(SWEInterval, self).__init__(iterable, **attribs)


class SWEConstraint(SWEBase):
    xml_tag = "constraint"


class SWEAllowedValues(SWEBase):
    xml_tag = "AllowedValues"

    def __init__(self, data):
        attrs = {}
        if hasattr(data, "getparent"):
            attrs.update(data.attrib)
            limit = []
        elif isinstance(data, dict):
            limit = data.get('interval', [])
        else:
            raise ValueError()
        setattr(self, "interval", SWEInterval(limit))
        super(SWEAllowedValues, self).__init__(**attrs)


class SWEDataRecord(SWEBase):
    xml_tag = "DataRecord"


if __name__ == "__main__":
    from lxml.etree import Element
    root = Element("root")
    root.text = "0 76000"
    # interval = SWEInterval(root)
    allow = SWEAllowedValues(root)
    print(9900)
    # print(interval)