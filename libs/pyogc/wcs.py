import xmltodict
from core.base import BaseWCS
from libs.pyogc.ogc.gml.gml import *


class WCS(BaseWCS):
    envelope = {}
    limits = {}

    def describe_coverage(self, coverage_id, **kwargs):
        self._get_data_from_server(coverageId=coverage_id, request="DescribeCoverage", **kwargs)

        # order(self.xml)
        for element in self.xml.iter():
            if element.prefix.lower() == "gml":
                # GML Elements
                namespace = "{%s}" % element.nsmap['gml'].lower()
                # obj = GMLBase.initialize_elements(element)

                if "%s%s" % (namespace, "boundedby") in element.tag.lower():
                    self.bounded_by = GMLBoundedBy(element)
                print(element)

        dct = xmltodict.parse(self.data.content)
        # remove_attrs_in_dict(dct)
        self.attributes = []
        if 'wcs:CoverageDescriptions' in dct:
            # TODO: SWE class that retrieves a list of coverage attributes
            for coverage_key in dct['wcs:CoverageDescriptions'].keys():
                if isinstance(coverage_key, basestring) and coverage_key.startswith('@'):
                    continue
                coverage_dct = {}
                coverage_desc = dct['wcs:CoverageDescriptions'][coverage_key]
                coverage_dct['name'] = coverage_desc['@id']
                coverage_dct['bands'] = []

                bounded_by = coverage_desc.get('gml:boundedBy', {})
                envelope = bounded_by.get('gml:Envelope', {})
                labels = envelope.get('@axisLabels', '').split(' ')
                lower_corner = envelope.get('gml:lowerCorner', "").split(' ')
                upper_corner = envelope.get('gml:upperCorner', "").split(' ')
                self.limits[labels[0]] = [lower_corner[0], upper_corner[0]]
                self.limits[labels[1]] = [lower_corner[1], upper_corner[1]]
                range_type = coverage_desc.get('gmlcov:rangeType', {})
                record = range_type.get('swe:DataRecord', {})
                time_period = coverage_desc.get('gml:TimePeriod', {})

                self.start_date = time_period.get('gml:beginPosition', None)
                self.end_date = time_period.get('gml:endPosition', None)
                self.period = time_period.get('gml:timeInterval', None)

                fields = record.get('swe:field', {})
                for field in fields:
                    # field = record[field_key]
                    coverage_dct['bands'].append(field['@name'])
                self.attributes.append(coverage_dct)

    def get_coverage(self, coverage_id, **kwargs):
        self._get_data_from_server(coverageID=coverage_id, request="GetCoverage", **kwargs)
        dct = xmltodict.parse(self.data.content)
        if 'gmlcov:GridCoverage' in dct:
            grid = dct['gmlcov:GridCoverage']
            self.values = grid['gml:rangeSet']['gml:DataBlock']['gml:tupleList']['#text']
            envelope = grid['gml:boundedBy']['gml:Envelope']
            start_date_point = envelope['gml:lowerCorner'].split(' ')[-1]
            end_date_point = envelope['gml:upperCorner'].split(' ')[-1]
            self.envelope["time_period"] = [start_date_point, end_date_point]
            # self.values = values_string.lstrip().split(',')
        else:
            self.values = ""

#
if __name__ == "__main__":
    wcs = WCS("http://127.0.0.1:8000/ows/", version="2.0.1")
    wcs.describe_coverage("mcd43a4")
# wcs.get_coverage("mcd43a4")