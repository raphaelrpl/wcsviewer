import xmltodict
from core.base import BaseWCS


class WCS(BaseWCS):
    def describe_coverage(self, coverage_id, **kwargs):
        return "ToDO"

    def get_coverage(self, coverage_id, subset=None, rangesubset=None, format=None, **kwargs):
        self._get_data_from_server(coverageID=coverage_id, request="GetCoverage")
        dct = xmltodict.parse(self.data.content)
        if 'gmlcov:GridCoverage' in dct:
            self.values = dct['gmlcov:GridCoverage']['gml:rangeSet']['gml:DataBlock']['gml:tupleList']['#text']
            # self.values = values_string.lstrip().split(',')
        else:
            self.values = ""