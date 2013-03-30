import unittest
from scraper import TicketScraper

class MockResponse(object):
    
    def __init__(self, response):
        self._response = response
    
    def read(self):
        return self._response

class ScraperTest(unittest.TestCase):

    def setUp(self):
        self._ts = TicketScraper('http://www.example.com')
    
    def test_response(self):
        response = MockResponse('stuff')
        self._ts._parse_response(response)
        self.assertTrue(self._ts._queue[0] == 'http://www.example.com')
        
    def test_link_queue(self):
        response = MockResponse('<a href=\"www.wegottickets.com/searchresults/page/1/all\">')
        self._ts._parse_response(response)
        self.assertTrue(len(self._ts._queue) == 2)
        self.assertTrue(self._ts._queue[1] == "www.wegottickets.com/searchresults/page/1/all")
        
    def test_date(self):
        self._ts._event = "<h2>MOCKDATE</h2>"
        self.assertTrue(self._ts._date[0] == 'MOCKDATE')
        
    def test_price(self):
        self._ts._event = "&pound;MOCKPRICE<"
        self.assertTrue(self._ts._price[0] == 'MOCKPRICE')

    def test_title(self):
        self._ts._event = "<title>MOCKTITLE</title>"
        self.assertTrue(self._ts._title == 'MOCKTITLE')

    def test_venue(self):
        self._ts._event = ".*\"venuetown\">MOCKVENUE</span"
        self.assertTrue(self._ts._venue == 'MOCKVENUE')
    
if __name__== '__main__':
    
    unittest.main()
    