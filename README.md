# getgeoinfo
This project is for collection latitude/longitude for specific location based on address using OSM.

## How to run
```
1. Download getgeoinfo scripts using git client (git clone) or Web browser using OSM or GoogleMAP
❯ python3 getgeoinfo.py -h
usage: getgeoinfo.py [-h] [-a ADDRESS] [-t TIMEOUT] [-s] -m MAP [-b BULK_FILE]

python3 getgeoinfo.py -m "osm|googlemap" [ -a "address" | -b file]

optional arguments:
  -h, --help            show this help message and exit
  -a ADDRESS, --address ADDRESS
                        input address to be search
  -t TIMEOUT, --timeout TIMEOUT
                        setting TIMEOUT value
  -s, --ssl_verify_flag
                        setting ssl verify flag
  -m MAP, --map MAP     specify one map out of both(osm, googlemap)
  -b BULK_FILE, --bulk_file BULK_FILE
                        processing csv file
 
 
2. Download getgeoinfo scripts using git client (git clone) or Web browser using NaverMAP
❯ python3 geonavermap.py -h                                                                                                                           
usage: geonavermap.py [-h] [-a ADDRESS] [-t TIMEOUT] [-s] [-b BULK_FILE]

python3 getgeoinfo.py [ -a "address" | -b file]

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

## Sample
❯ cat sample.csv
No,Address
1,상동 길주로
2,하남 덕풍공원로
3,송파 잠실7동
4,벌교 원동안길

❯ python3 getgeoinfo.py  -m googlemap -b sample.csv

❯ cat sample.csv
No,Address,googlemap_addr,googlemap_latitude,googlemap_longitude
1,상동 길주로,"Gilju-ro, Wonmi-gu, Bucheon-si, Gyeonggi-do, South Korea",37.504939,126.7859443
2,하남 덕풍공원로,"Deokpunggongwon-ro, Deokpung-dong, Hanam-si, Gyeonggi-do, South Korea",37.53907,127.1991664
3,송파 잠실7동,"Jamsil-dong, Songpa-gu, Seoul, South Korea",37.51289879999999,127.0829932
4,벌교 원동안길,"Wondongan-gil, Beolgyo-eup, Boseong-gun, Jeollanam-do, South Korea",34.8404036,127.336674
>
