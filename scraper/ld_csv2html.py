#!/usr/bin/env python
import csv
csvReader = csv.reader(open('ld.csv'), delimiter=';', quotechar='"')
for row in csvReader:
    print '<div class="distro">'
    print '<h2><a href="' + row[1] + '">' + row[0] + '</a></h2>'
    print '<pre>' + row[3] + '</pre>'
    print '<div>' + row[2] + '</div>'
    print '</div>'