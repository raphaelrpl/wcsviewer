import xmltodict
from core.base import BaseWCS


class WCS(BaseWCS):
    def describe_coverage(self, coverage_id, **kwargs):
        self._get_data_from_server(coverageId=coverage_id, request="DescribeCoverage", **kwargs)
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
                range_type = coverage_desc.get('gmlcov:rangeType', {})
                record = range_type.get('swe:DataRecord', {})
                time_period = coverage_desc.get('gml:TimePeriod', {})

                self.start_date = time_period.get('gml:beginPosition', None)
                self.end_date = time_period.get('gml:endPosition', None)

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


            # self.values = values_string.lstrip().split(',')
        else:
            self.values = ""


wcs = WCS("http://127.0.0.1:8000/ows/", version="2.0.1")
wcs.describe_coverage("mcd43a4")
wcs.get_coverage("mcd43a4")