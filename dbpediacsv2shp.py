#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import shapefile
import unicodecsv

from os.path import basename, splitext

parser = argparse.ArgumentParser(description='Create shapefiles from CSV.')
parser.add_argument('shp', help='Source shapefile')
args = parser.parse_args()

w = shapefile.Writer(shapefile.POINT)
outrows = [['name', 'latitude', 'longitude', 'thumbnail']]

w.autoBalance = 1  # make sure gemoetry and attributes match
w.field('X', 'F', 10, 5)
w.field('Y', 'F', 10, 5)
w.field('Name', 'C', 50)


def extract_wp_val(s):
    """Cells may contain values such as {42.0056|42.0067}, use the 1st one in
    these cases.

    Doesn't affect values were alternates are not the whole value.
    """
    return s.strip().strip('{}').split('|')[0]


with open(args.shp, 'rb') as csvin:
    reader = unicodecsv.reader(csvin)
    headers = reader.next()
    idxname = headers.index('name')
    idxlon = headers.index('wgs84_pos#long')
    idxlat = headers.index('wgs84_pos#lat')
    idxthumb = headers.index('thumbnail')

    # the next 3 rows are metadata
    reader.next()
    reader.next()
    reader.next()

    for row in reader:
        name = extract_wp_val(row[idxname]).encode('utf-8')
        lon = extract_wp_val(row[idxlon])
        lat = extract_wp_val(row[idxlat])
        thumb = extract_wp_val(row[idxthumb])

        # skip NULL values
        if 'NULL' in [lat, lat, name]:
            continue

        # sanity checks
        lon = float(lon)
        lat = float(lat)
        if lon < -180 or lon > 180 or lat < -90 or lat > 90:
            continue

        # create shapefile point and record
        w.point(lon, lat)
        w.record(lon, lat, name)

        outrows.append([name, lat, lon, thumb])


# write shape and CSV file
fname = splitext(basename(args.shp))[0]
w.save('shapefiles/%s' % fname)

with open('shapefiles/%s.csv' % fname, 'wb') as csvout:
    writer = unicodecsv.writer(csvout)
    writer.writerows(outrows)