from libs.pyogc.ogc.gml.exceptions import GMLValueError
from libs.pyogc.ogc.gml.base import GMLRangeBase, GMLBase


class GMLLowerCorner(GMLRangeBase):
    xml_tag = "lowerCorner"


class GMLUpperCorner(GMLRangeBase):
    xml_tag = "upperCorner"


class GMLLow(GMLRangeBase):
    xml_tag = "low"


class GMLHigh(GMLRangeBase):
    xml_tag = "high"


class GMLTupleList(GMLBase):
    xml_tag = "tupleList"
    delimiter_band = " "
    delimiter_data = ","

    def __init__(self, data, bands_name=None):
        attrs = {}
        if isinstance(data, dict):
            attrs.update(data.get('attributes', {}) or data.get('attrs', {}))
            self.delimiter_band = data.get('cs', self.delimiter_band)
            self.delimiter_data = data.get('ts', self.delimiter_data)
            values = (data.get("values", "") or data.get('text', "")).split(self.delimiter_data)
            output = {}
            if bands_name is not None:
                cont = 0
                for band in bands_name:
                    output[band] = []
                    for row in values:
                        values_band_list = row.lstrip(' ').split(self.delimiter_band)
                        output[band].append(values_band_list[cont])
                    cont += 1
                self.values = output
            # TODO: Values per each band
            # bands_size = values[0].split(self.delimiter_band)
        super(GMLTupleList, self).__init__(**attrs)

class GMLDataBlock(GMLBase):
    xml_tag = "DataBlock"


class GMLRangeSet(GMLBase):
    xml_tag = "rangeSet"

    def __init__(self, data):
        attrs = {}
        if isinstance(data, dict):
            attrs.update(data.get('attributes', {}) or data.get('attrs', {}))
        super(GMLRangeSet, self).__init__(**attrs)


class GMLGrid(GMLBase):
    xml_tag = "Grid"


class GMLEnvelope(GMLBase):
    xml_tag = "Envelope"

    def __init__(self, data, **attributes):
        super(GMLEnvelope, self).__init__(**attributes)
        if isinstance(data, dict):
            min_value = data.get('min')
            max_value = data.get('max')
            if min_value is None or max_value is None:
                raise GMLValueError("Excepted dict with \'min\' and \'max\' keys, but {0}".format(data))
            self.data = data
        elif hasattr(data, "getparent"):
            self.element = data
            for node in data:
                namespace = "{%s}" % node.nsmap['gml'].lower()
                if ("%s" % namespace + "lowercorner") == node.tag.lower():
                    node_name, attribs = self._prepare_node(node, namespace)
                    setattr(self, self.format_attr(node_name), GMLLowerCorner(node))
                elif ("%s" % namespace + "uppercorner") == node.tag.lower():
                    node_name, attribs = self._prepare_node(node, namespace)
                    setattr(self, self.format_attr(node_name), GMLUpperCorner(node))
                elif ("%s" % namespace + "low") == node.tag.lower():
                    node_name, attribs = self._prepare_node(node, namespace)
                    setattr(self, self.format_attr(node_name), GMLLowerCorner(node))
                elif ("%s" % namespace + "high") == node.tag.lower():
                    node_name, attribs = self._prepare_node(node, namespace)
                    setattr(self, self.format_attr(node_name), GMLUpperCorner(node))
                else:
                    raise GMLValueError("Error: Invalid type")

    @classmethod
    def _prepare_node(cls, node, namespace):
        node_name = node.tag.replace(namespace, '')
        return node_name, node.attrib


class GMLGridEnvelope(GMLEnvelope):
    xml_tag = "GridEnvelope"


class GMLBoundedBy(GMLBase):
    xml_tag = "boundedBy"

    def __init__(self, data):
        attrs = {}
        super(GMLBoundedBy, self).__init__(**attrs)
        # TODO: check if instance is element
        if hasattr(data, "getchildren"):
            self.element = data
            for node in data:
                namespace = node.nsmap['gml'].lower()
                if "{%s}%s" % (namespace, "envelope") in node.tag.lower():
                    attribs = node.attrib
                    self.envelope = GMLEnvelope(node, **attribs)