import ssl
import certifi
import geopy
import argparse
from geopy.geocoders import Nominatim

class Getgeoinfo():
    """
    This Getgeoinfo class contains getting latitude/longitude
    of specific addres from OSM(OpenStreetMap)
    """

    def __init__(self, address=None, timeout=None, ssl_verify_flag=False):
        self.address = args.address
        self.timeout = args.timeout
        self.ssl_verify_flag = args.ssl_verify_flag

        print(args)

    def ssl_verify(self, flag=False):
        if not flag:
            certx = ssl.create_default_context()
            certx.check_hostname = False
            certx.verify_mode = ssl.CERT_NONE
        else:
            certx = ssl.create_default_context(cafile=certifi.where())

        geopy.geocoders.options.default_ssl_context = certx
    
    def get_latlong(self)->dict():
        self.ssl_verify(self.ssl_verify_flag)
        _user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6)' \
                      'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                      'Chrome/71.0.3578.98 Safari/537.36'

        try:
            _n = Nominatim(user_agent=_user_agent, timeout=self.timeout)
            _x = _n.geocode(self.address)
        except Exception as e:
            print(str(e))
            return None

        if not _x:
            return None

        return {'address':_x.address.encode('utf-8'), 
                'lat':_x.latitude, 'long':_x.longitude}

if __name__ == "__main__":
    arg_parse = argparse.ArgumentParser(description='python3 getgeoinfo.py -i address')
    arg_parse.add_argument('-a', '--address', type=str, action='store',
                            required=False, help='input address to be search')
    arg_parse.add_argument('-t', '--timeout', type=int, default=10, 
                            required=False, help='setting TIMEOUT value')
    arg_parse.add_argument('-s', '--ssl_verify_flag', default=False, action='store_true',
                            required=False, help='setting ssl verify flag')
    args = arg_parse.parse_args()

    o_geo = Getgeoinfo()
    geo_result = o_geo.get_latlong()
    if not geo_result:
        print('Failed when searching geo location for this address')

    print(geo_result['address'].decode('utf-8'),
          geo_result['lat'], geo_result['long'])