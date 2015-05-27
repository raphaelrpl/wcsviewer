from wcs import WCS
import xmltodict


if __name__ == "__main__":
    print("**** GetCapabilities ****")
    w = WCS(url="http://127.0.0.1:8000/ows")
    w.get_capabilities()
    print("**** Status: %s ****" % w.data.status_code)
    print("**** Output *****")
    print(xmltodict.parse(w.data.content))