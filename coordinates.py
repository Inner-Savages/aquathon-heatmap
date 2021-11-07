import math

tileSize = 320
initialResolution = 2 * math.pi * 6378137 / tileSize
# 156543.03392804062 for tileSize 256 pixels
originShift = 2 * math.pi * 6378137 / 2.0
# 20037508.342789244


def LatLonToMeters( lat, lon ):
        "Converts given lat/lon in WGS84 Datum to XY in Spherical Mercator EPSG:900913"

        mx = lon * originShift / 180.0
        my = math.log( math.tan((90 + lat) * math.pi / 360.0 )) / (math.pi / 180.0)

        my = my * originShift / 180.0
        return mx, my


def MetersToPixels( mx, my, zoom):
        "Converts EPSG:900913 to pyramid pixel coordinates in given zoom level"

        res = initialResolution / (2**zoom)
        px = (mx + originShift) / res
        py = (my + originShift) / res
        return px, py

def PixelsToMeters( px, py, zoom):
    "Converts pixel coordinates in given zoom level of pyramid to EPSG:900913"

    res = initialResolution / (2**zoom)
    mx = px * res - originShift
    my = py * res - originShift
    return mx, my

def MetersToLatLon( mx, my ):
    "Converts XY point from Spherical Mercator EPSG:900913 to lat/lon in WGS84 Datum"

    lon = (mx / originShift) * 180.0
    lat = (my / originShift) * 180.0

    lat = 180 / math.pi * (2 * math.atan(math.exp(lat * math.pi / 180.0)) - math.pi / 2.0)
    return lat, lon


def dawaj_lewy_gorny(lat, lon, zoom):
    # lat_kuba = 53.118580
    # lon_kuba = 17.961935
    meter_x, meter_y = LatLonToMeters(lat, lon)
    pixel_x, pixel_y = MetersToPixels(meter_x, meter_y, zoom)
    pixel_xx = pixel_x - tileSize
    pixel_yy = pixel_y + tileSize

    # left_upper_corner of picture
    meter_xx, meter_yy = PixelsToMeters(pixel_xx, pixel_yy, zoom)
    llx, lly = MetersToLatLon(meter_xx, meter_yy)
    return llx, lly


def dawaj_kordy_dla_pixela(lat, lon, x, y, zoom):
    meter_x, meter_y = LatLonToMeters(lat, lon)
    pixel_x, pixel_y = MetersToPixels(meter_x, meter_y, zoom)
    pixel_xx = pixel_x - tileSize + x
    pixel_yy = pixel_y + tileSize - y

    # left_upper_corner of picture
    meter_xx, meter_yy = PixelsToMeters(pixel_xx, pixel_yy, zoom)
    llx, lly = MetersToLatLon(meter_xx, meter_yy)
    return llx, lly
