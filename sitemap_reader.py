from __future__ import with_statement  # we'll use this later, has to be here
import lxml
from argparse import ArgumentParser

import requests
from bs4 import BeautifulSoup as Soup

def parse_sitemap(url):
    resp = requests.get(url, verify=False)

    # we didn't get a valid response, bail
    if 200 != resp.status_code:
        return False

    # BeautifulStoneSoup to parse the document
    soup = Soup(resp.content, features="xml")

    # find all the <url> tags in the document
    urls = soup.findAll('url')

    # no urls? bail
    if not urls:
        return False

    # storage for later...
    out = []

    # extract what we need from the url
    for u in urls:
        item_url = u.find('loc').string
        out.append(item_url)
    return out


if __name__ == '__main__':
    options = ArgumentParser()
    options.add_argument('-u', '--url', action='store', dest='url', help='The file contain one url per line')
    options.add_argument('-o', '--output', action='store', dest='out', default='out.txt',
                         help='Where you would like to save the data')
    args = options.parse_args()
    urls = parse_sitemap(args.url)
    if not urls:
        print('There was an error!')
    with open(args.out, 'w') as out:
        out.write('\n'.join(urls))