import ssl
import certifi
import geopy
import argparse
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.geocoders import GoogleV3

GOOGLE_APIKEY = ""
MAPS = ['osm', 'googlemap']
class Getgeoinfo():
    """
    This Getgeoinfo class contains getting latitude/longitude
    of specific addres from OSM(OpenStreetMap)
    """

    def __init__(self, address=None, timeout=None, ssl_verify_flag=False):
        self.pasrge_argument()

        self.address = self.args.address
        self.timeout = self.args.timeout
        self.ssl_verify_flag = self.args.ssl_verify_flag
        self.bulk_file = self.args.bulk_file

        print(self.args)

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


        if self.map == 'osm':
            _m = Nominatim(user_agent=_user_agent, timeout=self.timeout)
        elif self.map == 'googlemap':
            if not GOOGLE_APIKEY:
                print('[*] Google API KEY has to be speicfy in code')
                return False
            _m = GoogleV3(api_key=GOOGLE_APIKEY)
        
        if self.address:
            try:
                _x = _m.geocode(self.address)
            except Exception as e:
                print(str(e))
                return None
    
            if not _x:
                return None
    
            return {'address':_x.address.encode('utf-8'), 
                    'lat':_x.latitude, 'long':_x.longitude}

        elif self.bulk_file:
            try:
                _df = pd.read_csv(self.bulk_file)
                _df[self.map+'_addr'] = _df['Address'].apply(_m.geocode)

                _df[self.map+'_latitude'] = _df[self.map+'_addr'].apply(lambda x: x.latitude
                                     if x else None) 

                _df[self.map+'_longitude'] = _df[self.map+'_addr'].apply(lambda x: x.longitude
                                     if x else None) 

                _df.to_csv(self.bulk_file,
                            sep=',', 
                            index=False)
                return _df.to_dict('records')

            except Exception as e:
                print(str(e))
                return None
    
    def pasrge_argument(self):
        arg_parse = argparse.ArgumentParser(description='python3 getgeoinfo.py'
                                            ' -m "osm|googlemap"' 
                                            ' [ -a "address" | -b file]')
        arg_parse.add_argument('-a', '--address', type=str, action='store',
                                required=False, help='input address to be search')
        arg_parse.add_argument('-t', '--timeout', type=int, default=10, 
                                required=False, help='setting TIMEOUT value')
        arg_parse.add_argument('-s', '--ssl_verify_flag', default=False, action='store_true',
                                required=False, help='setting ssl verify flag')
        arg_parse.add_argument('-m', '--map', type=str, action='store',
                                required=True, help='specify one map out of both(osm, googlemap)')
        arg_parse.add_argument('-b', '--bulk_file', default=False, action='store',
                                required=False, help='processing csv file')

        self.args = arg_parse.parse_args()
        self.args = arg_parse.parse_args()

        self.map = self.args.map.lower()

        if not self.map in MAPS:
            print('This {} map doesn\'t support'.format(self.map))
            return False

if __name__ == "__main__":
    o_geo = Getgeoinfo()
    geo_result = o_geo.get_latlong()

    if not geo_result:
        print('Failed when searching geo location for this address')
        exit(0)

    if not o_geo.bulk_file:
        print(geo_result['address'].decode('utf-8'),
              geo_result['lat'], geo_result['long'])
    else:
        print(geo_result)
