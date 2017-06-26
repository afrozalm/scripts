from bs4 import BeautifulSoup
import shutil
import urllib2
import os
import json
from multiprocessing.dummy import Pool
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-real', action='store_true')
option = parser.parse_args()

if not option.real:
    DIR = '../scraped_data2/'
    DST = '../scraped_data/'
    QUERY_SUFFIX = ' caricature'
else:
    DIR = '../scraped_data_real2/'
    DST = '../scraped_data_real/'
    QUERY_SUFFIX = ' face'


def get_soup(url, header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url, headers=header)),
                         'html.parser')


def scrape(celeb, limit=20):
    global DIR, DST, QUERY_SUFFIX
    ActualImages = []
    header = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64)"
              + " AppleWebKit/537.36 (KHTML, like Gecko)"
              + " Chrome/43.0.2357.134 Safari/537.36"}

    image_type = '_'.join(celeb.split())
    query = celeb.lower() + QUERY_SUFFIX
    query = query.split()
    query = '+'.join(query)

    for startIndex in range(1, 2):
        url = "https://www.google.co.in/search?q=" + query + \
            "&start=" + str(startIndex) + "&source=lnms&tbm=isch"
        print url
        soup = get_soup(url, header)

        for a in soup.find_all("div", {"class": "rg_meta"}):
            link, Type = json.loads(a.text)["ou"], json.loads(a.text)["ity"]
            ActualImages.append((link, Type))

    limit = min(len(ActualImages), limit)
    ActualImages = ActualImages[:limit]
    local_DIR = os.path.join(DIR, query.split()[0])

    if not os.path.exists(local_DIR):
        os.mkdir(local_DIR)

    for i, (img, Type) in enumerate(ActualImages):
        try:
            req = urllib2.Request(img, headers={'User-Agent': header})
            raw_img = urllib2.urlopen(req).read()

            cntr = len([i for i in os.listdir(local_DIR) if image_type in i]) + 1
            print cntr
            if len(Type) == 0:
                f = open(os.path.join(local_DIR, image_type +
                                      "_" + str(cntr) + ".jpg"), 'wb')
            else:
                f = open(os.path.join(local_DIR, image_type +
                                      "_" + str(cntr) + "." + Type), 'wb')

            f.write(raw_img)
            f.close()
        except Exception as e:
            print "could not load : " + img
            print e

if not os.path.exists(DIR):
    os.mkdir(DIR)
else:
    for d in os.listdir(DIR):
        try:
            shutil.move(os.path.join(DIR, d), DST)
        except:
            pass

with open('new_celebs.txt') as f:
    celebs = f.read()

celebs = celebs.split('\n')
celebs = set(celebs)
celebs.remove('')
print celebs
pool = Pool(7)
pool.map(scrape, celebs)
pool.close()
pool.join()
