# getgeoinfo
This project is for collection latitude/longitude for specific location based on address using OSM.

## How to run
```
1. Download getgeoinfo scripts using git client (git clone) or Web browser
❯ python3 getgeoinfo.py -h
usage: getgeoinfo.py [-h] [-a ADDRESS] [-t TIMEOUT] [-s] [-b BULK_FILE]

python3 getgeoinfo.py -i address

optional arguments:
  -h, --help            show this help message and exit
  -a ADDRESS, --address ADDRESS
                        input address to be search
  -t TIMEOUT, --timeout TIMEOUT
                        setting TIMEOUT value
  -s, --ssl_verify_flag
                        setting ssl verify flag
  -b BULK_FILE, --bulk_file BULK_FILE
                        processing csv file
```
