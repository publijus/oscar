import os
import sys
import django
from pathlib import Path
import random
import string
from decimal import Decimal
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from django.db import transaction
import requests
import traceback

# Nustatome kelią iki projekto šakninio katalogo
BASE_DIR = Path(__file__).resolve().parent

# Pridedame projekto šakninį katalogą į Python kelią
sys.path.append(str(BASE_DIR))

# Nustatome Django nustatymų modulį
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

# Inicializuojame Django
django.setup()

from oscar.apps.catalogue.models import Product, ProductClass, Category, ProductImage
from oscar.apps.partner.models import Partner, StockRecord
from oscar.apps.address.models import Country
from oscar.core.loading import get_model
from django.conf import settings
from django.db.utils import IntegrityError

print("Skriptas pradeda veikti...")

User = get_user_model()
Order = get_model('order', 'Order')
Line = get_model('order', 'Line')
ShippingAddress = get_model('order', 'ShippingAddress')

def get_random_car_part_image():
    try:
        width = 800
        height = 600
        image_id = random.randint(1, 1000)
        url = f"https://picsum.photos/id/{image_id}/{width}/{height}"
        response = requests.get(url)
        if response.status_code == 200:
            return ContentFile(response.content, name=f'product_{random.randint(1000, 9999)}.jpg')
        else:
            print(f"Nepavyko gauti paveikslėlio. Statusas: {response.status_code}")
            return None
    except Exception as e:
        print(f"Klaida gaunant paveikslėlį: {e}")
        return None

def generate_unique_upc():
    while True:
        upc = ''.join(random.choices(string.digits, k=13))
        if not Product.objects.filter(upc=upc).exists():
            return upc

@transaction.atomic
def create_categories():
    try:
        auto_parts = Category.add_root(name='Automobilių dalys')
        print(f"Sukurta pagrindinė kategorija: {auto_parts}")

        main_categories = {
            'Variklio sistema': ['Variklio blokas', 'Cilindrų galvutė', 'Stūmokliai', 'Alkūninis velenas'],
            'Stabdžių sistema': ['Stabdžių diskai', 'Stabdžių kaladėlės', 'ABS sistema'],
            'Važiuoklės sistema': ['Amortizatoriai', 'Spyruoklės', 'Svirties'],
            'Elektros sistema': ['Generatorius', 'Starteris', 'Akumuliatorius'],
            'Kėbulo dalys': ['Sparnai', 'Bamperiai', 'Durys'],
            'Salono detalės': ['Sėdynės', 'Prietaisų skydelis', 'Kilimėliai'],
            'Transmisijos sistema': ['Pavarų dėžė', 'Sankaba', 'Kardaninis velenas'],
            'Aušinimo sistema': ['Radiatorius', 'Termostatas', 'Aušinimo skysčio siurblys']
        }

        categories = {}
        for main_cat, sub_cats in main_categories.items():
            cat = auto_parts.add_child(name=main_cat)
            categories[main_cat] = cat
            print(f"Sukurta subkategorija: {cat}")
            
            for sub_cat in sub_cats:
                sub = cat.add_child(name=sub_cat)
                categories[f"{main_cat} - {sub_cat}"] = sub
                print(f"Sukurta trečio lygio kategorija: {sub}")

        category_count = Category.objects.count()
        print(f"Iš viso kategorijų: {category_count}")
        return categories
    except Exception as e:
        print(f"Klaida kuriant kategorijas: {e}")
        print(traceback.format_exc())
        return {}

def create_products(categories):
    try:
        partner, _ = Partner.objects.get_or_create(name='Auto Detalės')
        product_class, _ = ProductClass.objects.get_or_create(
            name='Automobilio detalės',
            requires_shipping=True
        )

        products_data = [
            ('Stabdžių diskas', 'Stabdžių sistema - Stabdžių diskai', 45.99, 'Aukštos kokybės stabdžių diskas'),
            ('Amortizatorius', 'Važiuoklės sistema - Amortizatoriai', 89.99, 'Patikimas amortizatorius'),
            ('Generatorius', 'Elektros sistema - Generatorius', 129.99, 'Galingas generatorius'),
            ('Variklio galvutė', 'Variklio sistema - Cilindrų galvutė', 299.99, 'Tvirta variklio galvutė'),
            ('Priekinis sparnas', 'Kėbulo dalys - Sparnai', 79.99, 'Lengvas priekinis sparnas'),
            ('Sėdynių užvalkalai', 'Salono detalės - Sėdynės', 49.99, 'Patogūs sėdynių užvalkalai'),
            ('Pavarų dėžė', 'Transmisijos sistema - Pavarų dėžė', 599.99, 'Automatinė pavarų dėžė'),
            ('Radiatorius', 'Aušinimo sistema - Radiatorius', 109.99, 'Efektyvus radiatorius'),
        ]

        car_brands = ['BMW', 'Audi', 'Volkswagen', 'Mercedes-Benz', 'Toyota', 'Ford', 'Opel', 'Volvo']

        created_products = 0
        for i in range(50):
            try:
                product_base = random.choice(products_data)
                brand = random.choice(car_brands)
                title = f"{brand} {product_base[0]}"
                category = categories.get(product_base[1])
                if not category:
                    print(f"Kategorija nerasta: {product_base[1]}")
                    continue
                price = Decimal(product_base[2]) + Decimal(random.randint(-10, 10))
                
                upc = generate_unique_upc()
                product, created = Product.objects.get_or_create(
                    upc=upc,
                    defaults={
                        'title': title,
                        'product_class': product_class,
                        'description': f"{product_base[3]} tinkantis {brand} automobiliams."
                    }
                )
                
                if created:
                    product.categories.add(category)
                    
                    # Pridedame 3 nuotraukas kiekvienam produktui
                    for _ in range(3):
                        image = get_random_car_part_image()
                        if image:
                            ProductImage.objects.create(product=product, original=image)
                        else:
                            print(f"Nepavyko pridėti paveikslėlio produktui: {product}")
                    
                    StockRecord.objects.create(
                        product=product,
                        partner=partner,
                        partner_sku=upc,
                        price_currency='EUR',
                        price=price,
                        num_in_stock=random.randint(0, 100)
                    )
                    created_products += 1
                    print(f"Sukurtas naujas produktas: {product}")
                else:
                    print(f"Produktas su UPC {upc} jau egzistuoja: {product}")
            except Exception as e:
                print(f"Klaida kuriant produktą: {e}")
                print(traceback.format_exc())

        print(f"Sukurta {created_products} naujų produktų.")
    except Exception as e:
        print(f"Klaida kuriant produktus: {e}")
        print(traceback.format_exc())

def populate_countries():
    try:
        for code, name in settings.OSCAR_SHOP_COUNTRIES:
            Country.objects.get_or_create(
                iso_3166_1_a2=code,
                defaults={'printable_name': name}
            )
        print("Šalys sėkmingai sukurtos arba atnaujintos.")
    except Exception as e:
        print(f"Klaida kuriant šalis: {e}")
        print(traceback.format_exc())

def create_orders():
    try:
        users = User.objects.all()
        if not users:
            User.objects.create_user('customer@example.com', 'password')
            users = User.objects.all()

        products = Product.objects.all()
        country = Country.objects.get(iso_3166_1_a2='LT')

        created_orders = 0
        for i in range(10):
            try:
                user = random.choice(users)
                order_number = f'1000{Order.objects.count() + 1}'
                order = Order.objects.create(
                    user=user,
                    number=order_number,
                    status='Completed',
                    total_incl_tax=Decimal('0.00'),
                    total_excl_tax=Decimal('0.00')
                )
                
                # Sukuriame ShippingAddress objektą
                shipping_address = ShippingAddress.objects.create(
                    first_name=user.first_name or "Vardenis",
                    last_name=user.last_name or "Pavardenis",
                    line1='Gatvės g. 1',
                    line4='Vilnius',
                    postcode='01234',
                    country=country
                )
                
                # Priskiriame ShippingAddress prie užsakymo
                order.shipping_address = shipping_address
                order.save()
                
                for _ in range(random.randint(1, 5)):
                    product = random.choice(products)
                    stockrecord = product.stockrecords.first()
                    quantity = random.randint(1, 3)
                    price = stockrecord.price
                    
                    Line.objects.create(
                        order=order,
                        product=product,
                        partner_sku=stockrecord.partner_sku,
                        stockrecord=stockrecord,
                        quantity=quantity,
                        line_price_incl_tax=price * quantity,
                        line_price_excl_tax=price * quantity,
                        line_price_before_discounts_incl_tax=price * quantity,
                        line_price_before_discounts_excl_tax=price * quantity,
                        unit_price_incl_tax=price,
                        unit_price_excl_tax=price,
                        unit_retail_price=price,
                    )
                
                order.total_incl_tax = sum(line.line_price_incl_tax for line in order.lines.all())
                order.total_excl_tax = sum(line.line_price_excl_tax for line in order.lines.all())
                order.save()
                created_orders += 1
                print(f"Sukurtas užsakymas: {order}")
            except IntegrityError:
                print(f"Klaida kuriant užsakymą: užsakymo numeris jau egzistuoja")
            except Exception as e:
                print(f"Klaida kuriant užsakymą: {e}")
                print(traceback.format_exc())

        print(f"Sukurta {created_orders} naujų užsakymų.")
    except Exception as e:
        print(f"Klaida kuriant užsakymus: {e}")
        print(traceback.format_exc())

if __name__ == "__main__":
    try:
        categories = create_categories()
        create_products(categories)
        populate_countries()
        create_orders()
        print("Duomenų atnaujinimas baigtas!")
    except Exception as e:
        print(f"Klaida vykdant skriptą: {e}")
        print(traceback.format_exc())
    finally:
        print("Skriptas baigė darbą.")