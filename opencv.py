from PIL import Image
import matplotlib.cm
import numpy as np
from math import sqrt
from downloaderStatic import download
import simplekml as KML
from coordinates import dawaj_kordy_dla_pixela

# how many pixels in one slice
height = 32
width = 32

def zapisz_mi_to_na_mape(k, lat, lon, x, y, kolor, zoom):
    global width, height
    pol = k.newpolygon(name='polygon')
    a = dawaj_kordy_dla_pixela(lat, lon, x, y, zoom)
    b = dawaj_kordy_dla_pixela(lat, lon, x + width, y, zoom)
    c = dawaj_kordy_dla_pixela(lat, lon, x + width, y + height, zoom)
    d = dawaj_kordy_dla_pixela(lat, lon, x, y + height, zoom)
    pol.outerboundaryis = [(a[1], a[0]), (b[1], b[0]), (c[1], c[0]), (d[1], d[0])]
    pol.style.polystyle.outline = 0
    pol.style.polystyle.color = KML.Color.hexa(hex(kolor[0])[2:] + hex(kolor[1])[2:] +hex(kolor[2])[2:] + '80')
    return True

def prepareColors(kml, lat, lng):
    # download single satellite image from Google Maps
    satimg = download(lat, lng, 19)

    # open image instead
    # satimg = Image.open("high_resolution_image.png")

    w, h = satimg.size
    # final = Image.new('RGBA', (w, h))

    colormap = matplotlib.cm.get_cmap('RdYlGn_r')
    for i in range(0, h, height):
        for j in range(0, w, width):
            box = (j, i, j+width, i+height)
            crop = satimg.crop(box)
            pixels = crop.load()
            cropwidth, cropheight = crop.size
            all_pixels = []
            for x in range(cropwidth):
                for y in range(cropheight):
                    cpixel = pixels[x, y]
                    distance = sqrt(cpixel[0] ** 2 + (cpixel[1] - 170) ** 2 + cpixel[2] ** 2)
                    if distance > 255:
                        distance = 255
                    all_pixels.append(distance)
            all_pixels.sort()
            median = all_pixels[len(all_pixels) // 2]
            map_of_colors = colormap([i for i in range(256)])
            map_of_colors2 = np.uint8(map_of_colors * 255)
            color = map_of_colors2[int(median)]
            zapisz_mi_to_na_mape(kml, lat, lng, j, i, color, 19)
            # im = Image.new(mode='RGBA', size=(width, height), color=tuple(color))
            # im = im.convert('RGB')
            # tile = Image.blend(crop, im, 0.9)
            # final.paste(tile, (j, i))
    # return final
    return True

startinglat = 53.129890523656655
startinglon = 18.00002953253117
lon = startinglon
for i in range(5):
    lat = startinglat
    kml = KML.Kml()
    for j in range(3):
        prepareColors(kml, lat, lon)
        lat, lon = dawaj_kordy_dla_pixela(lat, lon, 320, 960, 19)
    kml.save(f'kwadracik_{i}.kml')
    print(f'kwadracik_{i}.kml')
    lat, lon = dawaj_kordy_dla_pixela(lat, lon, 960, 320, 19)
