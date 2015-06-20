from libs.pyogc.ogc.gml.exceptions import GMLValueError
from libs.pyogc.ogc.gml.base import GMLRangeBase, GMLBase


class GMLLowerCorner(GMLRangeBase):
    pass


class GMLUpperCorner(GMLRangeBase):
    pass


class GMLLow(GMLRangeBase):
    pass


class GMLHigh(GMLRangeBase):
    pass


class GMLTupleList(GMLBase):
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
            if bands is not None:
                cont = 0
                for band in bands:
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
    pass


class GMLRangeSet(GMLBase):
    def __init__(self, data):
        attrs = {}
        if isinstance(data, dict):
            attrs.update(data.get('attributes', {}) or data.get('attrs', {}))
        super(GMLRangeSet, self).__init__(**attrs)


class GMLGrid(GMLBase):
    pass


class GMLEnvelope(GMLBase):
    def __init__(self, data, **attributes):
        super(GMLEnvelope, self).__init__(**attributes)
        if isinstance(data, dict):
            min_value = data.get('min')
            max_value = data.get('max')
            if min_value is None or max_value is None:
                raise GMLValueError("Excepted dict with \'min\' and \'max\' keys, but {0}".format(data))
            self.data = data

            self._init_limits(min_value, max_value)

    def _init_limits(self, min_value, max_value):
        self.lower = GMLLowerCorner(min_value)
        self.upper = GMLUpperCorner(max_value)


class GMLGridEnvelope(GMLEnvelope):
    def _init_limits(self, min_value, max_value):
        self.low = GMLLow(min_value)
        self.high = GMLHigh(max_value)


# Dummy Data
data = {
    "min": {
        "values": [20, 30], "attrs": {
            "href": "microsoft.com"
        }
    },
    "max": {
        "values": [25, 35], "attrs": {
            "href": "americanas.com"
        }
    }
}

dct = {
    "attrs": {},
    "values": "2503 2007 2191, 4018 2504 4124, 2241 468 2477, 3667 3734 3397, 4980 2429 3000, 2365 3785 1003, 247 1641 627, 3919 677 2559, 788 3636 2770, 2402 3710 1269, 1034 998 3278, 4928 713 1589, 1899 638 2754, 1112 3687 1022, 2209 2611 4323, 2927 1872 3836, 3202 1977 3406, 2248 176 2405, 495 4354 550, 915 2337 4783, 1297 2794 1677, 1401 4732 3086, 3591 3245 1619, 2527 4908 836, 2 58 3885, 2491 4981 475, 3750 671 869, 4884 1030 4369, 2955 2687 2053, 4557 3164 2022, 1347 2895 646, 1170 3036 340, 4487 619 4186, 4926 1866 3413, 1331 1648 2811, 4476 4741 2074, 2123 4960 4162, 3321 1101 2071, 4255 3998 2382, 4114 4066 919, 277 2156 4057, 1683 4800 4953, 4097 4205 2224, 2284 699 1866, 2458 1814 4429, 402 1455 3513, 3725 4775 1980, 4887 1166 4994, 4569 436 539, 4990 2164 1718, 3625 4439 565, 2898 3842 520, 4049 1287 539, 4680 4611 917, 3800 1709 1018, 3195 2964 3042, 23 4330 3361, 408 4548 3218, 289 4539 2338, 1433 4567 260, 4597 2436 4988, 2702 1223 3681, 4829 704 189, 2284 4489 776, 3000 4799 4412, 1813 1695 3397, 2075 4588 3103, 1509 208 709, 597 2931 1518, 320 2083 4331, 3707 1988 1588, 3763 3713 1072, 1433 4985 866, 507 1668 4076, 2597 1344 321, 2053 4171 3822, 989 4803 1741, 362 3918 960, 1236 2980 3816, 2301 3965 1743, 193 3556 2815, 2743 1975 234, 3529 405 1368, 875 3269 1291, 3159 4171 2373, 2878 4477 4245, 1287 1337 3146, 595 4159 1861, 1725 236 1775, 1038 7 3482, 1296 4121 4929, 2161 776 4234, 3574 4315 2965, 2896 2657 1280, 600 526 2208, 1213 1206 3242, 1693 1046 4101, 2655 1265 3343, 3438 2334 84, 3030 3264 3698, 3044 4829 3643, 1620 732 3068, 3314 2804 443, 2847 1570 18, 2728 3341 3859, 559 2978 3661, 1166 1104 4178, 3879 4105 2908, 3016 2077 3203, 3611 2333 2087, 1020 2023 2355, 948 4947 4124, 4635 3008 1890, 2900 4400 2646, 3467 180 3164, 4543 2176 2879, 4045 1642 676, 3661 4799 4783, 2229 514 2202, 4568 368 2109, 4555 4680 694, 2688 4720 3008, 690 1406 4661, 4791 1456 2643, 147 3920 3606, 1676 2514 755, 1480 4468 4087, 814 1885 1607, 2635 1255 686, 1004 3973 3358, 4375 1826 3373, 2328 1466 612, 303 2202 2695, 1641 3215 1163, 881 4286 567, 3732 1757 772, 1063 2796 4490, 1032 1367 4918, 3299 4596 80, 3461 3249 2649, 4409 2967 1227, 4091 1341 3872, 2981 3648 2812, 590 2963 1420"
}

bands = ["red", "nir", "quality"]

envelope = GMLEnvelope(data=data, **{"href": "google.com"})
grid_envelope = GMLGridEnvelope(data, **{"href": "google.com"})

tuple_list = GMLTupleList(dct, bands)
print(envelope)