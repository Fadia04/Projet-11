from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver.common.by import By
import time
from products.models import Product, Category, Categorized


class TestSearchProduct(StaticLiveServerTestCase):
    def test_search(self):
        self.browser = webdriver.Chrome("purbeurre/tests/functional_tests/chromedriver")
        self.browser.get(self.live_server_url + reverse("home"))
        search_product = self.browser.find_element(By.NAME, "query")
        search_product.send_keys("nutella")
        search_button = self.browser.find_element(By.ID, "result-button")
        search_button.click()
        time.sleep(5)
        self.assertEqual(
            self.browser.find_element(By.TAG_NAME, "h1").text,
            "Voici les produits que vous avez demandés pour: nutella",
        )
        self.assertEqual(
            self.browser.current_url, self.live_server_url + reverse("results")
        )
        time.sleep(5)
        self.browser.close()

    def test_results(self):
        self.browser = webdriver.Chrome("purbeurre/tests/functional_tests/chromedriver")
        # self.browser.maximize_window()
        self.browser.get(self.live_server_url + reverse("home"))
        search_product = self.browser.find_element(By.NAME, "query")
        search_product.send_keys("nutella")

        prod1 = Product.objects.create(
            name="pur beurre de cacahuète",
            nutriscore="b",
            image="https://images.openfoodfacts.org/images/products/376/002/050/7350/front_fr.292.400.jpg",
            code=3760020507350,
            stores="casino",
            url=1,
        )
        prod2 = Product.objects.create(
            name="pâte à tartiner nutella noisettes et cacao - 200g",
            nutriscore="e",
            image="https://images.openfoodfacts.org/images/products/80135463/front_fr.168.400.jpg",
            code=80135463,
            stores="carrefour",
            url="2",
        )
        category1 = Category.objects.create(name="pates a tartiner")
        Categorized.objects.create(product_id=prod1, category_id=category1)
        Categorized.objects.create(product_id=prod2, category_id=category1)
        search_button = self.browser.find_element(By.ID, "result-button")
        search_button.click()
        time.sleep(5)
        self.browser.current_url, self.live_server_url + reverse("results")
        # results = self.browser.find_element(By.ID, "product-name")
        self.assertEqual(
            self.browser.find_element(By.TAG_NAME, "h4").text,
            "pur beurre de cacahuète",
            "nutella",
        )
        # self.assertEqual(self.browser.current_url, results[0])
        # self.browser.get(self.live_server_url + reverse("results"))
        # results = self.browser.find_element(By.ID, "product-name")
        # results = self.browser.find_element(By.ID, "résultats")
        # results.send_keys("pur beurre de cacahuètes")
        # self.assertEqual(self.browser.find_element(By.CLASS_NAME, "page-section"))
        # self.assertEqual(self.browser.find_element(By.ID, "product-name"))
        # self.browser.get(self.live_server_url)
        product_detail = self.live_server_url + reverse(
            "product_detail", args=[prod1.id]
        )
        detail_button = self.browser.find_element(
            By.LINK_TEXT, "pur beurre de cacahuète"
        )
        self.browser.execute_script("arguments[0].click();", detail_button)

        # detail_button = self.browser.find_element(By.ID, "product-name")
        # detail_button.send_keys("pur beurre de cacahuète")
        # detail_button.click()
        time.sleep(10)
        # self.assertEqual(product_detail)

        self.assertEqual(self.browser.current_url, product_detail)

        # self.assertEqual(self.browser.find_element(By.ID, "résultats"))

        # self.assertEqual(self.browser.find_element(By.TAG_NAME, "h1").text,
        # "Voici les produits que vous avez demandés:nutella")
        # self.assertEqual(self.browser.current_url, self.live_server_url + reverse("results"))

        # time.sleep(10)
        self.browser.close()
