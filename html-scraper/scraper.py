#!./bin/python3
import sys, getopt
from optparse import OptionParser
from bs4 import BeautifulSoup as bs
from urllib.request import (
    Request, urlopen, urlparse, urlunparse, urlretrieve)

visited = []

def create_request(url):
    req = Request(url)
    req.add_header("User-Agent", "Nico")
    req.add_header("Accept-Language", "en-GB,en-US;q=0.9,en;q=0.8")
    req.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8")
    return urlopen(req)


def scrape(url):

    # If the URL has already been scraped, ignore. In theory we should check the Last-Modified and Expires headers
    # as well to make sure the page hasn't changed in the meanwhile
    if url in visited:
        return

    parsed = urlparse(url)
    if not parsed.scheme:
        print("%s is not a valid URL. Please specify an http scheme (http or https)" % url)
        return

    if not parsed.netloc:
        print("'%s' is not a valid URL. Hostname missing", url)
        sys.exit(1)

    print("Scraping '%s'" % url)
    url_obj = create_request(url)
    visited.append(url)
    soup = bs(url_obj, features="html.parser")

    print("The title: " + soup.title.string)
    links = soup.findAll('a')
    for a in links:
        href = a.attrs["href"]
        print("link: ", href)
        if not href.startswith("#"):
             scrape(href)


def main (argv) :
    usage = "usage: prog% [options] arg1 arg2"
    parser = OptionParser(usage=usage, version="%prog 1.0")
    parser.add_option("-u", "--url", action="store", type="string", metavar="URL_STRING", dest="url",help="The URL to start the scraping from")
    parser.add_option("-v", "--verbose", action="store_true", default=False, dest="verbose", help="Whether to enable verbose logging (default: %default)")
    opts, args = parser.parse_args()

    if not opts.url:
        print("Please specify a URL")
        parser.print_help()
        sys.exit(1)

    scrape(opts.url)

# Call main
main(sys.argv[1:])

