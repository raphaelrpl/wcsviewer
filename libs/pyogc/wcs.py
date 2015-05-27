from core.base import BaseWCS


class WCS(BaseWCS):
    def describe_coverage(self, coverage_id, **kwargs):
        return "ToDO"

    def get_coverage(self, coverage_id, subset=None, rangesubset=None, format=None, **kwargs):
        self._get_data_from_server(coverageID=coverage_id)