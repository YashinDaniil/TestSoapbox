import json
import os
from dataclasses import dataclass, asdict

import shopify
from loguru import logger

shopify_api_key = os.getenv('API_KEY')
shopify_api_secret_key = os.getenv('API_SECRET_KEY')
shopify_api_access_key = os.getenv('ACCESS_TOKEN')
shopify_shop_name = os.getenv('SHOP_NAME')
api_version = os.getenv('API_VERSION') #2023-04


@dataclass
class ProductData:
    id: int
    title: str


@dataclass
class OrderData:
    id: int
    name: str
    total_price: float


class ShopifyClient:
    def __init__(self, api_key, api_secret_key, access_token, shop_name, api_version):
        self.API_KEY = api_key
        self.API_SECRET_KEY = api_secret_key
        self.ACCESS_TOKEN = access_token
        self.SHOP_NAME = shop_name
        self.API_VERSION = api_version
        self.shopify = None
        try:
            self.activate_session()
        except Exception as e:
            logger.error("Couldn't open the session")
            logger.error(e)
            self.shopify = None

    def activate_session(self):
        shopify.Session.setup(api_key=self.API_KEY, secret=self.API_SECRET_KEY)
        shop_url = f"{self.SHOP_NAME}.myshopify.com"
        session = shopify.Session(shop_url, self.API_VERSION, self.ACCESS_TOKEN)
        shopify.ShopifyResource.activate_session(session)
        self.shopify = shopify

    def get_products(self):
        try:
            products = self.shopify.Product.find()
        except Exception as e:
            logger.error(e)
            return []
        product_data = []
        for product in products:
            data = ProductData(id=product.id, title=product.title)
            product_data.append(data)
        return product_data

    def get_orders(self):
        try:
            orders = self.shopify.Order.find()
        except Exception as e:
            logger.error(e)
            return []
        order_data = []
        for order in orders:
            data = OrderData(id=order.id, name=order.name, total_price=float(order.total_price))
            order_data.append(data)
        return order_data


def format_shopify_dataclass_data(items_data):
    return json.dumps([asdict(item) for item in items_data], indent=4)


shopify_client = ShopifyClient(shopify_api_key, shopify_api_secret_key, shopify_api_access_key, shopify_shop_name,
                               api_version)

shopify_products = shopify_client.get_products()
shopify_orders = shopify_client.get_orders()

print(format_shopify_dataclass_data(shopify_products))
print(format_shopify_dataclass_data(shopify_orders))
