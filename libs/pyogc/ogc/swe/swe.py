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
        super(SWEInterval, self).__init__(iterable, **attribs)


class SWEConstraint(SWEBase):
    xml_tag = "constraint"


class SWEAllowedValues(SWEBase):
    xml_tag = "AllowedValues"


class SWEDataRecord(SWEBase):
    xml_tag = "DataRecord"