import urllib2
import urllib
import bs4
import time
import random
import os.path
from os import listdir
import zipfile
import xlrd

linkset = set()


def download_archive(link, folder):
    full = 'http://bvb.ro/' + link
    print 'downloading ' + full
    urllib.urlretrieve(full, '{0}/{1}'.format(folder, os.path.basename(full)[:-1]))


def download_archives(folder):
    with open('trades_list.txt', 'r') as f:
        files = f.readlines()
    if not os.path.exists(folder):
        os.makedirs(folder)
    for name in files:
        download_archive(name, folder)
        time.sleep(random.randint(1, 3))  # BE NICE :)


def add_to_download_set(date):
    u = 'http://bvb.ro/TradingAndStatistics/DailyMarketReport.aspx?d=' + date
    urllib2.urlopen(u)
    soup = bs4.BeautifulSoup(urllib2.urlopen(u).read())
    table = soup.findChildren('table', {'id': 'ctl00_central_listBVB'})  # soup.find_all('table', {'id': 'ctl00_central_listBVB'})
    print type(table)
    print len(table)
    links = table[0].findChildren('a')
    for link in links:
        linkset.add(link['href'])
        print link['href']


def build_download_set():
    for year in range(2012, 2015):
        for month in range(1, 13):
            add_to_download_set('{0}/15/{1}'.format(month, year))
            time.sleep(random.randint(1, 4))  # be nice :)

    with open('trades_list.txt', 'w') as f:
        for l in linkset:
            f.write(l + '\n')


def unzip_everything(in_folder, out_folder):
    files = listdir(in_folder)
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    for f in files:
        with zipfile.ZipFile('{0}/{1}'.format(in_folder, f)) as zf:
            zf.extractall(out_folder)


def process_xls(file):
    book = xlrd.open_workbook(file)
    print book.nsheets
    sheet = book.sheet_by_index(1)
    print sheet.cell(11, 1)


def main():
    #build_download_set()
    #download_archives('Trades')
    unzip_everything('Trades', 'TradesUnpacked')
    #TradesUnpacked/trades20111129.xls
    process_xls('TradesUnpacked/trades20111129.xls')


if __name__ == "__main__":
    main()