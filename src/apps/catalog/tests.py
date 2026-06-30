from django.test import TestCase

from apps.catalog.models import Category, Product


class CatalogModelsTestCase(TestCase):
    def test_category_and_product_can_be_created(self):
        category = Category.objects.create(name='Electronics', slug='electronics')
        product = Product.objects.create(
            name='Smartphone',
            slug='smartphone',
            description='A sample smartphone',
            price=999.99,
            sku='SKU-001',
            category=category,
            brand='Example Brand',
        )

        self.assertEqual(category.name, 'Electronics')
        self.assertEqual(product.category, category)
        self.assertTrue(product.is_active)
