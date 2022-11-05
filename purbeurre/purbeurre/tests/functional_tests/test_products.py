from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.service import Service


class TestSearchProduct(StaticLiveServerTestCase):
    def test_search(self):        
        # Add lines 12 and 13 and suppress line 14 to resolve this warning:DeprecationWarning: executable_path has been deprecated, please pass in a Service object
        #chrome_executable = Service(executable_path='chromedriver.exe', log_path='NUL')
        self.browser = webdriver.Chrome()        
        #self.browser = webdriver.Chrome("purbeurre/tests/functional_tests/chromedriver")
        self.browser.get(self.live_server_url + reverse("home"))
        search_product = self.browser.find_element(By.NAME, 'query')
        search_product.send_keys("nutella")
        search_button = self.browser.find_element(By.ID,"result-button")
        search_button.click()
        self.assertEqual(self.browser.find_element(By.TAG_NAME, "h1").text,
                         "Voici les produits que vous avez demandés:nutella")
        self.assertEqual(self.browser.current_url, self.live_server_url + reverse("results"))
        self.browser.close()   
        time.sleep(20)