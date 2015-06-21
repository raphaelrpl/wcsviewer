from unittest.case import TestCase
from libs.pyogc.wcs import WCS
from libs.pyogc.ogc.gml import GMLBoundedBy


class GMLTest(TestCase):
    def test_success(self):
        # Dummy Data
        wcs = WCS("http://127.0.0.1:8000/ows/", version="2.0.1")
        wcs.describe_coverage("mcd43a4e")
        self.assertIsInstance(getattr(wcs, 'bounded_by'), GMLBoundedBy)
