import ssl
import certifi
import argparse
import requests
import pandas as pd
import json

NAVERMAP_CLIENTID=""
NAVERMAP_SECRETKEY=""

class GeoNavermap():
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

    def ssl_verify(self, flag=False):
        if not flag:
            certx = ssl.create_default_context()
            certx.check_hostname = False
            certx.verify_mode = ssl.CERT_NONE
        else:
            certx = ssl.create_default_context(cafile=certifi.where())

    def navermap_v2(self, address):
        x_result = {}
        x_param = {'query': address} 

        navermapv2_uri = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"
        headers = {
            'User-Agent': self.user_agent,
            'X-NCP-APIGW-API-KEY-ID': NAVERMAP_CLIENTID,
            'X-NCP-APIGW-API-KEY': NAVERMAP_SECRETKEY
        }

        r = requests.get(navermapv2_uri, headers=headers, params=x_param, verify=False)
        result = r.json()
        
        if result['meta']['count']:
            x_result['navermap_addr'] = result['addresses'][0]['roadAddress']
            x_result['navermap_addr_en'] = result['addresses'][0]['englishAddress']
            x_result['navermap_longitude'] = result['addresses'][0]['x'] 
            x_result['navermap_latitude'] = result['addresses'][0]['x']
        else:
            x_result['navermap_addr'] = None
            x_result['navermap_addr_en'] = None
            x_result['navermap_longitude'] = None
            x_result['navermap_latitude'] = None

        return x_result
        
    def get_latlong(self)->dict():
        self.ssl_verify(self.ssl_verify_flag)
        self.user_agent =   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6)' \
                            'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                            'Chrome/71.0.3578.98 Safari/537.36'

        if self.address:
            try:
                _x = self.navermap_v2(self.address)
            except Exception as e:
                print(str(e))
                return None

            if not _x:
                return None

            return _x

        elif self.bulk_file:
            try:
                _df = pd.read_csv(self.bulk_file)
                _df['navermap_result'] = _df['Address'].apply(self.navermap_v2)

                _df['navermap_address'] = _df['navermap_result'].apply(lambda x: x['navermap_addr']
                                    if x else None) 
                _df['navermap_address_en'] = _df['navermap_result'].apply(lambda x: x['navermap_addr_en']
                                    if x else None) 
                _df['navermap_latitude'] = _df['navermap_result'].apply(lambda x: x['navermap_latitude']
                                    if x else None) 

                _df['navermap_longitude'] = _df['navermap_result'].apply(lambda x: x['navermap_longitude']
                                    if x else None) 

                _df = _df.drop(columns=['navermap_result'])

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
        arg_parse.add_argument('-b', '--bulk_file', default=False, action='store',
                                required=False, help='processing csv file')

        self.args = arg_parse.parse_args()
        self.args = arg_parse.parse_args()


if __name__ == "__main__":
    o_geo = GeoNavermap()
    geo_result = o_geo.get_latlong()

    if not geo_result:
        print('Failed when searching geo location for this address')
        exit(0)

    if not o_geo.bulk_file:
        """
        print(geo_result['address'].decode('utf-8'),
              geo_result['lat'], geo_result['long'])
              """
        print(geo_result)
    else:
        print(geo_result)
