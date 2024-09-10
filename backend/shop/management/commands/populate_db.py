from django.core.management.base import BaseCommand
from shop.models import Category, Product, PartType, PartOption, PriceRule
from django.contrib.auth.models import User
from django.db import transaction

class Command(BaseCommand):
    help = 'Populates the database with sample data'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write('Populating database...')

        # Create a test user
        user, created = User.objects.get_or_create(username='testuser', email='test@example.com')
        if created:
            user.set_password('testpassword')
            user.save()
            self.stdout.write(self.style.SUCCESS('Test user created'))

        # Create categories
        categories = ['Bicycles', 'Accessories', 'Components']
        for cat_name in categories:
            Category.objects.get_or_create(name=cat_name)

        # Create products
        products = [
            ('Mountain Bike', 'Bicycles', 500.00),
            ('Road Bike', 'Bicycles', 700.00),
            ('Helmet', 'Accessories', 50.00),
            ('Bike Light', 'Accessories', 30.00),
            ('Handlebar', 'Components', 80.00),
        ]

        for prod_name, cat_name, price in products:
            category = Category.objects.get(name=cat_name)
            product, created = Product.objects.get_or_create(
                name=prod_name,
                category=category,
                defaults={'base_price': price}
            )

            if cat_name == 'Bicycles':
                # Create part types and options for bicycles
                frame, _ = PartType.objects.get_or_create(name='Frame', product=product)
                PartOption.objects.get_or_create(name='Aluminum', part_type=frame, defaults={'price': 100.00})
                PartOption.objects.get_or_create(name='Carbon', part_type=frame, defaults={'price': 300.00})

                wheels, _ = PartType.objects.get_or_create(name='Wheels', product=product)
                PartOption.objects.get_or_create(name='26 inch', part_type=wheels, defaults={'price': 50.00})
                PartOption.objects.get_or_create(name='29 inch', part_type=wheels, defaults={'price': 100.00})

                brakes, _ = PartType.objects.get_or_create(name='Brakes', product=product)
                PartOption.objects.get_or_create(name='Disc', part_type=brakes, defaults={'price': 80.00})
                PartOption.objects.get_or_create(name='Rim', part_type=brakes, defaults={'price': 40.00})

        # Create a price rule
        mountain_bike = Product.objects.get(name='Mountain Bike')
        frame = PartType.objects.get(name='Frame', product=mountain_bike)
        wheels = PartType.objects.get(name='Wheels', product=mountain_bike)
        
        carbon_frame = PartOption.objects.get(name='Carbon', part_type=frame)
        big_wheels = PartOption.objects.get(name='29 inch', part_type=wheels)
        
        price_rule, _ = PriceRule.objects.get_or_create(price_adjustment=-50.00)
        price_rule.part_options.add(carbon_frame, big_wheels)

        self.stdout.write(self.style.SUCCESS('Database successfully populated'))