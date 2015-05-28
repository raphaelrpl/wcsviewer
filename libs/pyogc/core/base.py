from abc import ABCMeta, abstractmethod
from exceptions import WCSException, WCSRequestError, WCSInvalidParameter
import requests


class BaseWCS(object):
    __metaclass__ = ABCMeta
    url = None
    version = None
    service = "WCS"

    def __init__(self, url="http://geobrain.laits.gmu.edu/cgi-bin/ows8/wcseo", version="2.0.1"):
        if not url:
            raise WCSException("url is empty - \"%s\"" % url)
        if version not in ['2.0', '2.0.1']:
            raise WCSInvalidParameter(value=version)
        self.url = url
        self.version = version

    def _get_data_from_server(self, method="GET", **parameters):
        parameters['service'] = self.service
        parameters['version'] = self.version
        parameters['request'] = parameters.get('request')
        if method == "GET":
            self.data = requests.get(self.url, params=parameters)
        elif method == "POST":
            self.data = requests.post(self.url, params=parameters)
        else:
            raise WCSRequestError("Invalid request method - \"%s\"" % method)

    def get_capabilities(self, **kwargs):
        self._get_data_from_server(request="GetCapabilities")
        return self.data

    @abstractmethod
    def describe_coverage(self, coverage_id, **kwargs):
        """
        :param coverage_id: a string or a list of coverage identifier -> e.g 'mcd43a4'
        :param kwargs:
        :return:
        """

    @abstractmethod
    def get_coverage(self, coverage_id, subset=None, rangesubset=None, format=None, **kwargs):
        """
        It must to be implemented
        """