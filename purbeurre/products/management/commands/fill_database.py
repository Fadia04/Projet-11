from itertools import product
from unicodedata import category
from urllib import response
from django.core.management.base import BaseCommand
from products.models import Product
from products.models import Category
from products.models import Categorized
import requests

class Command(BaseCommand):
    help = 'Populate database pur_beurre with OFF products'
    
    
    def handle(self, *args, **kwargs):
        req = requests.get( "https://fr.openfoodfacts.org/cgi/search.pl", {"action": "process",
                    "sort_by": "unique_scans_n",
                    "page_size": 100,
                    "page": 1,
                    "json": 1
                })
        response = req.json()["products"] 
        for data in response:
            if data.get("product_name_fr") and data.get("url") and data.get('categories') and data.get("stores") and data.get("nutriscore_grade"):
                product = Product.objects.get_or_create(
                name = data.get("product_name_fr").lower(),
                url = data.get("url").lower(),
                image = data.get("image_url"),
                stores = data.get("stores").lower(),
                nutriscore = data.get("nutriscore_grade").lower(),
                code = data.get("code"))
                self.insert_category(data.get('categories'), product)
                
        self.stdout.write('Database succesfully populated')
        
    def insert_category(self, categories, product_id):
        categories = categories.lower()
        categories = categories.split(',')
        for i in range(len(categories)):
            if "en:" in categories[i]:
                categories[i] = categories[i].replace("en:", " ")  
        for category in categories:
            category_id = Category.objects.get_or_create(name = category.strip())
            Categorized.objects.get_or_create(product_id = product_id[0], category_id = category_id[0]) 
            
    
    #def insert_category(self, categories):
        #categories = categories.lower()
        #categories = categories.split(',') 
        #for i in range(len(categories)):
                    #if "en:" in categories[i]:
                        #categories[i] = categories[i].replace("en:", " ") 
        #for category in categories:
            #category = Category.objects.get_or_create(name = category.strip()) 
            #self.insert_categorized(categories, product)
    #def insert_categorized(self, category_id, product_id):
        #for product_id in product:
            #Categorized.objects.get_or_create(product_id = id_product) 
            #for category_id in category:  
                #category_id = Category.objects.get_or_create(name = category.strip())      
                #Categorized.objects.get_or_create(category_id = category_id, product_id = product_id) 
    
    
    """
    products = []
    cleaned_products = []
    
    def _get_products(self):
        
        req = requests.get( "https://fr.openfoodfacts.org/cgi/search.pl", {"action": "process",
                    "sort_by": "unique_scans_n",
                    "page_size": 10,
                    "page": 1,
                    "json": 1
                })
        response = req.json()["products"]
        for data in response:
            self.products.append(data)
        
    def _cleaner_products(self):
        
            #Function to select from the products #downloaded only those containing the five #chosen attributes.
            #These data will then be formatted
        
    
        for data in self.products:
            if data.get("product_name_fr") and data.get("url") and data.get('categories') and data.get("stores") and data.get("nutriscore_grade"):
                name = data.get("product_name_fr").lower()
                url= data.get("url").lower()
                categories = data.get('categories').lower()
                categories = data.get('categories').split(",")
               
                for i in range(len(categories)):
                    if "'" in categories[i]:
                        categories[i] = categories[i].replace("'", " ")
                stores = data.get("stores").lower()
                nutriscore = data.get("nutriscore_grade").lower()               
                self.cleaned_products = Product.objects.create(name = name, url = url, categories = categories, stores = stores, nutriscore = nutriscore)
                #self.cleaned_products.append(data)
                
                                                       
    def handle(self, *args, **kwargs):
        self._cleaner_products()
        self.stdout.write('Database succesfully populated')
    """