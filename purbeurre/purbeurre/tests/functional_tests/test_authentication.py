from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time


class TestAuthentification(StaticLiveServerTestCase):
    def test_open_chrome_window(self):
        self.browser = webdriver.Chrome("purbeurre/tests/functional_tests/chromedriver")
        self.browser.get(self.live_server_url)
        time.sleep(5)
        self.browser.close()
      
