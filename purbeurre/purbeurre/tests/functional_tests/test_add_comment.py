from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver.common.by import By
import time
from products.models import Product, Category, Categorized


class TestAddComment(StaticLiveServerTestCase):
    def test_add_comment(self):
        self.browser = webdriver.Chrome("purbeurre/tests/functional_tests/chromedriver")

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
        self.assertEqual(
            self.browser.find_element(By.TAG_NAME, "h4").text, "pur beurre de cacahuète"
        )
        

        product_detail = self.live_server_url + reverse(
            "product_detail", args=[prod1.id]
        )
        detail_button = self.browser.find_element(
            By.LINK_TEXT, "pur beurre de cacahuète"
        )
        self.browser.execute_script("arguments[0].click();", detail_button)
        self.assertEqual(self.browser.current_url, product_detail)
        time.sleep(5)

        # comments = self.browser.get(self.live_server_url + reverse("add-comment", args=[prod1.id]))
        comments = self.live_server_url + reverse("add-comment", args=[prod1.id])
        # comment = self.browser.find_element(By.NAME, 'comment_body')
        # comment.send_keys("commentaire")
        comment_butt = self.browser.find_element(By.LINK_TEXT, "Ajouter")
        self.browser.execute_script("arguments[0].click();", comment_butt)
        # comment_butt.click()
        time.sleep(5)
        self.assertEqual(
            self.browser.find_element(By.TAG_NAME, "h2").text, "Ajoutez un commentaire"
        )
        self.assertEqual(self.browser.current_url, comments)
        add_comment = self.browser.find_element(By.NAME, "comment_body")
        add_comment.send_keys("Ce produit est assez intéressant pour remplacer la pâte à tartiner nutella, notamment pour son nutriscore assez faible et bien sûr son goût exqui")
        save_comment = self.live_server_url + reverse("product_detail", args=[prod1.id])
        save_comment_button = self.browser.find_element(By.ID, "add-comment-button")
        self.browser.execute_script("arguments[0].click();", save_comment_button)
        # save_comment_button.click()
        time.sleep(10)

        self.assertEqual(self.browser.current_url, save_comment)
        self.browser.close()
        time.sleep(20)
