import unittest
from ..lib import scrape_twitter


class TestLoginTwitter(unittest.TestCase):
    def test_single_account(self):
        # Input username and password
        username = 'yantoriu12'
        password = 'Miksa211'
        scrape = scrape_twitter.ScrapeTwitter(username, password, "Viral")
        
