import unittest
import os

from home_work import ShopifyClient, ProductData, format_shopify_dataclass_data

shopify_api_key = os.getenv('API_KEY')
shopify_api_secret_key = os.getenv('API_SECRET_KEY')
shopify_api_access_key = os.getenv('ACCESS_TOKEN')
shopify_shop_name = os.getenv('SHOP_NAME')
api_version = os.getenv('API_VERSION')  # 2023-04


class Tests(unittest.TestCase):
    def setUp(self):
        print("\nRunning setUp method...")
        self.shopify_client = ShopifyClient(shopify_api_key, shopify_api_secret_key, shopify_api_access_key,
                                            shopify_shop_name,
                                            api_version)

    def test_activation(self):
        self.assertTrue(self.shopify_client.shopify)

    def test_get_orders(self):
        orders = self.shopify_client.get_orders()
        self.assertTrue(len(orders) > 1)

    def test_get_products(self):
        products = self.shopify_client.get_products()
        self.assertTrue(len(products) > 1)

    def test_output_data(self):
        test_data = [ProductData(id=1, title='test1'), ProductData(id=2, title='test2')]
        data = format_shopify_dataclass_data(test_data)
        self.assertEqual(data, '''[
    {
        "id": 1,
        "title": "test1"
    },
    {
        "id": 2,
        "title": "test2"
    }
]'''
                         )
