import pandas as pd
from shop.models import Store, Region, Product
from userauth.models import SalesUser
import random as rand
from django.db.models.functions import Cast
from django.db.models.fields import TextField, CharField
from django.db import transaction

df = pd.read_csv("games_shoppe/Products.csv")
products_data = df.to_dict('records')

regions_data = list(Region.objects.annotate(uid=Cast("id", output_field=CharField())).values_list("uid","name"))

regions_d = {key: val for key, val in regions_data}

region_keys = list(regions_d.keys())


def get_region():
    return rand.choice(region_keys)

all_stores = list(set(df['store'].to_list()))



stores_data = list(Store.objects.filter(name__in=all_stores).annotate(uid=Cast("id", output_field=TextField())).values_list("uid", "name"))
stores_d = {val: key for key, val in stores_data}

def get_store_id(storename):
    return stores_d[storename]


with transaction.atomic():
    product_blk_qs = [ Product(name=item['name'], store_id=get_store_id(item['store']),category=item['category'], inventory=item['inventory'],original_cost=item['original_cost'], price=item['price'],image_url=item['imageUrl']) for item in products_data]
    Product.objects.bulk_create(product_blk_qs)
    
