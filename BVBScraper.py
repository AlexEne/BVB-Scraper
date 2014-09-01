import urllib2
import urllib
import bs4
import time
import random
import os.path


linkset = set()


def download_archive(link):
    fullLink = 'http://bvb.ro/' + link
    print 'downloading %s' % fullLink
    urllib.urlretrieve(fullLink, 'Trades/'+os.path.basename(fullLink)[:-1])


def download_archives():
    with open('trades_list.txt', 'r') as f:
        files = f.readlines()
    for name in files:
        download_archive(name)
        time.sleep(random.randint(1, 3))


def add_to_download_set(date):
    u = 'http://bvb.ro/TradingAndStatistics/DailyMarketReport.aspx?d=' + date
    urllib2.urlopen(u)
    soup = bs4.BeautifulSoup(urllib2.urlopen(u).read())
    table = soup.findChildren('table', {
        'id': 'ctl00_central_listBVB'})  # soup.find_all('table', {'id': 'ctl00_central_listBVB'})
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


def main():
    # 12/14/2013
    #/info/SumareDeTranzactionare/BSE/2013/trades20130308.zip
    #download_archives('/info/SumareDeTranzactionare/BSE/2013/trades20130308.zip')
    build_download_set()
    download_archives()



if __name__ == "__main__":
    main()