# -*- coding: utf-8 -*-
import pandas as pd
import shapefile
import argparse

from os.path import basename, splitext

parser = argparse.ArgumentParser(description='Create shapefiles from CSV.')
parser.add_argument('shp', help='Source shapefile')
args = parser.parse_args()

w = shapefile.Writer(shapefile.POINT)

w.autoBalance = 1  # make sure gemoetry and attributes match
w.field('X', 'F', 10, 5)
w.field('Y', 'F', 10, 5)
w.field('Name', 'C', 50)

df = pd.read_csv(args.shp)
for l in df.iterrows():
    lat = l[1]['latitude']
    lon = l[1]['longitude']
    name = l[1]['name']
    w.point(lon, lat)
    w.record(lon, lat, name)

fname = splitext(basename(args.shp))[0]
w.save('shapefiles/%s' % fname)