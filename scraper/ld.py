#!/usr/bin/env python
import re
import csv
from pyquery import PyQuery as pq


def get_doc(url):
    try:
        doc = pq(url=url)
        return doc
    except:
        return False


def get_meta(doc, name):
    selector = 'meta[name=' + name + ']'
    meta = doc(selector)
    return meta.attr('content')


def match_twitter(e):
    href = e.attr('href')
    if href is not None and re.search('twitter.com/\w+', href):
        return href
    return None


def find_twitter_urls(doc):
    twitter_urls = []
    for a in doc('a'):
        twitter_url = match_twitter(pq(a))
        if twitter_url is not None:
            twitter_urls.append(twitter_url)
    return twitter_urls


def distro(e):
    global csvWriter
    desc = None
    a = e('a')
    website = a.attr('href')
    name = a.text()
    doc = get_doc(website)
    if doc is not False:
        # try to fetch meta description from website
        desc = get_meta(doc, 'description')
        if desc is None:
            # take description from linuxlinks.com
            desc = e('div').text()

        # search for links to twitter in content
        twitter_urls = find_twitter_urls(doc)
        twitter_urls = "\n".join(twitter_urls)

        print website + "\n"
        csvWriter.writerow([name, website, desc.encode('utf-8'), twitter_urls])


doc = get_doc('http://www.linuxlinks.com/Distributions/')
if doc is not False:
    csvWriter = csv.writer(open('ld.csv', 'w'), delimiter=';', quotechar='"')
    doc('ul[type=DISC] li').each(distro)