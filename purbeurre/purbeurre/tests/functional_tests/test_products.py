from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver.common.by import By
import time


class TestSearchProduct(StaticLiveServerTestCase):
    def test_search(self):
        self.browser = webdriver.Chrome("purbeurre/tests/functional_tests/chromedriver")
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