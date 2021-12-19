import geocoder
import csv

def initial():
    with open('data/latlng.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['場所', '緯度', '経度'])

def fetch_latlng():

    l = []
    
    with open('data/latlng.csv') as f:
        reader = csv.reader(f)
        l = [row for row in reader]

    l_T = [list(x) for x in zip(*l)]

    n = l_T[0]

    for i in range(1, n):
        location = l_T[i]
        ret = geocoder.osm(location, timeout=5.0)
        lat = ret.latlng[0]
        lng = ret.latlng[1]

        with open('data/latlng.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow([location, lat, lng])