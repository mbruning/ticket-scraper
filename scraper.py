from collections import deque
import urllib2
import re
import json
import sys

class TicketScraper(object):
    
    LINKREGEX = re.compile('<a.*href=\"(.*wegottickets.*searchresults.*)\">')
    EVENTREGEX = re.compile('<a.*href=\"(.*)\" class=\"event_link\">')
    TITLEREGEX = re.compile('<title>(.*)</title>')
    VENUEREGEX = re.compile('.*\"venuetown\">(.*)</span')
    DATEREGEX = re.compile('<h2>(.*)</h2>')
    PRICEREGEX = re.compile('&pound;([^\<]*)\<')
    
    def __init__(self, base_url):
        self._base_url = base_url
        self._queue = deque()
        self._queue.append(base_url)
        self._visited = []
        
    def scrape(self):
        while True:
            try:
                _next = self._queue.popleft()
            except:
                break
            self._visited.append(_next)
            try:
                self._parse_response(urllib2.urlopen(_next))
            except Exception:
                continue
            
    def _parse_response(self, response):
        resp = response.read()
        self._extract_concerts(resp)
        links = self.LINKREGEX.findall(resp)
        for l in links:
            self._store_link(l)
            
    def _store_link(self, link):
        if not link in self._queue and not link in self._visited:
            self._queue.append(link)
            return True
        return False
        
    def _extract_concerts(self, response):
        events = self.EVENTREGEX.findall(response)
        for e in events:
            try:
                self._event = urllib2.urlopen(e).read()
            except Exception, e:
                print e
                continue
            try:
                town, venue = self._venue.split(':')
            except:
                venue = self._venue
                town = venue
                venue = venue
            print json.dumps({'title': self._title,
                              'town': town,
                              'venue': venue,
                              'date': self._date,
                              'price': self._price})
            
    @property
    def _date(self):
        date = self.DATEREGEX.findall(self._event)
        if date:
            return date
        else:
            return "Not found"
        
    @property
    def _price(self):
        price = self.PRICEREGEX.findall(self._event)
        return price
                
    @property
    def _title(self):
        title = self.TITLEREGEX.findall(self._event)
        return title[0].split('-')[-1]
            
    @property
    def _venue(self):
        venue = self.VENUEREGEX.findall(self._event)
        try:
            return re.sub(r'<.*>', '', venue[0])
        except:
            return "Not found"
            
if __name__ == "__main__":

    BASE_URL = "http://www.wegottickets.com/searchresults/page/1/all"
        
    ts = TicketScraper(BASE_URL)
    try:
        ts.scrape()
    except KeyboardInterrupt:
        sys.exit()
    