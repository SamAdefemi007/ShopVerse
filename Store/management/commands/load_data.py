import os
import random
import csv
from sqlite3 import Cursor
from turtle import title
from unicodedata import decimal
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from Store.models import Customer, Products, Collection, Category, Order, OrderItem
from pathlib import Path
from faker import Faker


class Command(BaseCommand):
    help = 'loads the product catalog into the database'

    def handle(self, *args, **options):
        for table in [Order, OrderItem, Products, Customer, Collection, Category, Order, CartItem, Cart]:
            table.objects.all().delete()

        print("Tables dropped successfully")

        base_dir = Path(__file__).resolve().parent.parent.parent.parent

        # loading the products catalog into the database

        with open(str(base_dir) + '/Store/data/products.csv', newline='') as file:
            reader = csv.reader(file, delimiter=",")
            next(reader)  # skip the header line
            collection_list, category_list = [], []
            for row in reader:
                if row[14] not in collection_list:
                    collection_list.append(row[14])
                    collection_object = Collection.objects.create(
                        title=row[14]
                    )
                    collection_object.save()
                else:
                    collection_object = Collection.objects.get(title=row[14])

                if row[15] not in category_list:
                    category_list.append(row[15])
                    category_object = Category.objects.create(
                        title=row[15]
                    )
                    category_object.save()
                else:
                    category_object = Category.objects.get(title=row[15])

                Products.objects.create(
                    size=row[0],
                    brand=row[1],
                    unit_price=float(row[12]),
                    discounted_price=float(row[13]),
                    image=row[7],
                    title=row[4],
                    material=row[3],
                    care=row[2],
                    color=row[6],
                    details=row[9],
                    style=row[11],
                    kind=row[15],
                    fit=row[10],
                    Rating=row[17],
                    collection=collection_object,
                    category=category_object,)

# # creating customer details in the database
        fake = Faker()

        for i in range(10, 25):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = first_name+last_name

            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=fake.ascii_free_email(),
                password='P@ssWorD123',
                username=username
            )

            customer = Customer.objects.get(
                user=user
            )
            customer.phone = fake.phone_number(),
            customer.birth_date = fake.date()

            customer.save()

        # # creating orders and orderItem from customer details and products

            customer_object = Customer.objects.all()
            product_list = Products.objects.all()
            product = list(product_list)
            for customer in customer_object:
                randproduct = random.randint(0, len(product))
                rand_num = random.randrange(1, 15)
                for i in range(rand_num):
                    choices = ["P", "C", "F"]
                    rand_choice = random.randrange(0, 3)
                    status = choices[rand_choice]
                    Order.objects.create(
                        customer=customer,
                        payment_status=status,
                        order_placed_at=fake.date_between(
                            start_date='-1y', end_date='today')
                    )

                order_object = Order.objects.all()
                product_list = Products.objects.all()
                product = list(product_list)
                for order in order_object:
                    randproduct = random.randint(0, len(product)-1)
                    OrderItem.objects.create(
                        order=order,
                        product=product[randproduct],
                        quantity=random.randint(1, 10),
                    )

        print("data parsed successfully")
