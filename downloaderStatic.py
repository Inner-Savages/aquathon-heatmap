import requests
from PIL import Image

key = ""

def download(lat, lng, zoom=19, size="640x640"):
    url = "https://maps.googleapis.com/maps/api/staticmap?center=" \
          + str(lat) + "," + str(lng) + \
          "&zoom=" + str(zoom) + "&size=" + size + \
          "&maptype=satellite&key=" \
          + key
    r = requests.get(url, stream=True)
    r.raw.decode_content = True
    return Image.open(r.raw).convert('RGB')

if __name__ == '__main__':
    download(53.118580, 17.961935, 19)
