from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from catering.models import Category, CateringPackage, MenuItem
from orders.models import Cart, Order, Review

# Source photos live as static assets (frontend/static/img/rasaganga/) — this
# command opens them and uploads the bytes through whichever MEDIA storage
# backend is active (local disk in dev, Cloudinary in production), instead
# of assuming a local file path, so seeding works the same way everywhere.
SOURCE_IMAGES_DIR = Path(settings.FRONTEND_DIR) / 'static' / 'img' / 'rasaganga'


def _attach_image(instance, field_name, source_filename, upload_as):
    source_path = SOURCE_IMAGES_DIR / source_filename
    with open(source_path, 'rb') as f:
        getattr(instance, field_name).save(upload_as, File(f), save=False)
    instance.save(update_fields=[field_name])


class Command(BaseCommand):
    help = 'Seed the database with The Rasaganga catering categories, menu, and packages.'

    def handle(self, *args, **options):
        # Re-seeding replaces the whole catalog, so any test bookings against
        # the old packages have to go first (OrderItem/Review protect their package FK).
        Review.objects.all().delete()
        Order.objects.all().delete()
        Cart.objects.all().delete()

        CateringPackage.objects.all().delete()
        MenuItem.objects.all().delete()
        Category.objects.all().delete()

        categories_data = [
            ('Wedding', 'Grand South Indian vegetarian spreads for the big day.', 'food5.jpg', 'wedding.jpg'),
            ('Birthday Party', 'Fun tiffin and chaat combos for birthday celebrations.', 'food2.jpg', 'birthday-party.jpg'),
            ('Corporate Event', 'Quick, professional tiffin box catering for meetings.', 'food4.jpg', 'corporate-event.jpg'),
            ('Festival', 'Traditional thalis and sweets for festive occasions.', 'exterior.jpg', 'festival.jpg'),
        ]
        categories = {}
        for name, desc, source_image, upload_as in categories_data:
            category = Category.objects.create(name=name, description=desc)
            _attach_image(category, 'image', source_image, upload_as)
            categories[name] = category

        # Real à la carte menu — transcribed from The Rasaganga's own menu boards.
        # (name, section, food_type, price)
        menu_items_data = [
            # Idly & Vada
            ('Rice Idly (2 Nos.)', 'Idly & Vada', MenuItem.FoodType.STARTER, 40),
            ('Rava Idly', 'Idly & Vada', MenuItem.FoodType.STARTER, 40),
            ('Thatte Idly', 'Idly & Vada', MenuItem.FoodType.STARTER, 50),
            ('Uddina Vada', 'Idly & Vada', MenuItem.FoodType.STARTER, 30),
            ('Masala Vada', 'Idly & Vada', MenuItem.FoodType.STARTER, 40),
            ('Maddur Vada', 'Idly & Vada', MenuItem.FoodType.STARTER, 40),
            ('Dahi Vada', 'Idly & Vada', MenuItem.FoodType.STARTER, 40),
            # Dosa Varieties
            ('Plain Dosa', 'Dosa Varieties', MenuItem.FoodType.MAIN_COURSE, 50),
            ('Masala Dosa', 'Dosa Varieties', MenuItem.FoodType.MAIN_COURSE, 60),
            ('Set Dosa', 'Dosa Varieties', MenuItem.FoodType.MAIN_COURSE, 60),
            ('Rava Dosa', 'Dosa Varieties', MenuItem.FoodType.MAIN_COURSE, 70),
            ('Onion Dosa', 'Dosa Varieties', MenuItem.FoodType.MAIN_COURSE, 70),
            ('Rava Masala Dosa', 'Dosa Varieties', MenuItem.FoodType.MAIN_COURSE, 70),
            ('Ragi Dosa', 'Dosa Varieties', MenuItem.FoodType.MAIN_COURSE, 70),
            ('Butter Masala Dosa', 'Dosa Varieties', MenuItem.FoodType.MAIN_COURSE, 70),
            ('Paper Masala Dosa', 'Dosa Varieties', MenuItem.FoodType.MAIN_COURSE, 80),
            ('Mysore Masala Dosa', 'Dosa Varieties', MenuItem.FoodType.MAIN_COURSE, 80),
            # Chaat & Street Food
            ('Masala Puri', 'Chaat & Street Food', MenuItem.FoodType.STARTER, 40),
            ('Bhel Puri', 'Chaat & Street Food', MenuItem.FoodType.STARTER, 40),
            ('Pani Puri', 'Chaat & Street Food', MenuItem.FoodType.STARTER, 40),
            ('Dahi Puri', 'Chaat & Street Food', MenuItem.FoodType.STARTER, 50),
            ('Sev Puri', 'Chaat & Street Food', MenuItem.FoodType.STARTER, 50),
            ('Samosa Masala', 'Chaat & Street Food', MenuItem.FoodType.STARTER, 50),
            ('Vada Pav', 'Chaat & Street Food', MenuItem.FoodType.STARTER, 40),
            ('Pav Bhaji', 'Chaat & Street Food', MenuItem.FoodType.MAIN_COURSE, 80),
            ('Paneer Pav Bhaji', 'Chaat & Street Food', MenuItem.FoodType.MAIN_COURSE, 90),
            # Indo-Chinese
            ('Veg Fried Rice', 'Indo-Chinese', MenuItem.FoodType.MAIN_COURSE, 70),
            ('Paneer Fried Rice', 'Indo-Chinese', MenuItem.FoodType.MAIN_COURSE, 80),
            ('Veg Noodles', 'Indo-Chinese', MenuItem.FoodType.MAIN_COURSE, 70),
            ('Veg Fried Noodles', 'Indo-Chinese', MenuItem.FoodType.MAIN_COURSE, 80),
            ('Spring Roll', 'Indo-Chinese', MenuItem.FoodType.STARTER, 90),
            # Thali & Meals
            ('Roti Curry', 'Thali & Meals', MenuItem.FoodType.MAIN_COURSE, 50),
            ('South Indian Thali', 'Thali & Meals', MenuItem.FoodType.MAIN_COURSE, 140),
            ('North Indian Thali', 'Thali & Meals', MenuItem.FoodType.MAIN_COURSE, 160),
            ('Rasaganga Spl Thali', 'Thali & Meals', MenuItem.FoodType.MAIN_COURSE, 220),
            # Beverages & Juices
            ('Filter Coffee', 'Beverages & Juices', MenuItem.FoodType.BEVERAGE, 30),
            ('Fresh Lime Soda', 'Beverages & Juices', MenuItem.FoodType.BEVERAGE, 50),
            ('Sweet Lassi', 'Beverages & Juices', MenuItem.FoodType.BEVERAGE, 50),
            ('Salt Lassi', 'Beverages & Juices', MenuItem.FoodType.BEVERAGE, 50),
            ('Butter Milk', 'Beverages & Juices', MenuItem.FoodType.BEVERAGE, 30),
            ('Mango Juice (Seasonal)', 'Beverages & Juices', MenuItem.FoodType.BEVERAGE, 50),
            ('Musambi Juice', 'Beverages & Juices', MenuItem.FoodType.BEVERAGE, 50),
            # Sweets
            ('Gulab Jamun', 'Sweets', MenuItem.FoodType.DESSERT, 40),
            ('Rava Kesari', 'Sweets', MenuItem.FoodType.DESSERT, 40),
            ('Payasam', 'Sweets', MenuItem.FoodType.DESSERT, 50),
        ]
        menu_items = {}
        for name, section, food_type, price in menu_items_data:
            menu_items[name] = MenuItem.objects.create(
                name=name, section=section, food_type=food_type, is_veg=True, price=price,
            )

        def m(*names):
            return [menu_items[n] for n in names]

        packages_data = [
            (
                'Rasaganga Wedding Thali', 'Wedding', 599, 100, 1000,
                m('Rasaganga Spl Thali', 'South Indian Thali', 'North Indian Thali', 'Payasam', 'Gulab Jamun', 'Filter Coffee'),
                'food5.jpg', 'rasaganga-wedding-thali.jpg',
            ),
            (
                'Filter Coffee & Tiffin Breakfast', 'Wedding', 349, 50, 500,
                m('Masala Dosa', 'Rava Idly', 'Masala Vada', 'Filter Coffee'),
                'food4.jpg', 'filter-coffee-tiffin-breakfast.jpg',
            ),
            (
                'Birthday Chaat & Snacks Combo', 'Birthday Party', 299, 20, 150,
                m('Pani Puri', 'Bhel Puri', 'Sev Puri', 'Pav Bhaji', 'Fresh Lime Soda'),
                'food2.jpg', 'birthday-chaat-snacks-combo.jpg',
            ),
            (
                'Kids Dosa Party', 'Birthday Party', 199, 15, 80,
                m('Plain Dosa', 'Masala Dosa', 'Vada Pav', 'Payasam'),
                'food3.jpg', 'kids-dosa-party.jpg',
            ),
            (
                'Corporate Tiffin Box', 'Corporate Event', 249, 10, 200,
                m('Rava Idly', 'Masala Vada', 'Pav Bhaji', 'Filter Coffee'),
                'food4.jpg', 'corporate-tiffin-box.jpg',
            ),
            (
                'Boardroom Filter Coffee Meet', 'Corporate Event', 199, 10, 100,
                m('Uddina Vada', 'Samosa Masala', 'Filter Coffee'),
                'food2.jpg', 'boardroom-filter-coffee-meet.jpg',
            ),
            (
                'Indo-Chinese Corporate Combo', 'Corporate Event', 279, 15, 150,
                m('Veg Fried Rice', 'Spring Roll', 'Veg Noodles', 'Sweet Lassi'),
                'food1.jpg', 'indo-chinese-corporate-combo.jpg',
            ),
            (
                'Festival Sweets & Savouries Thali', 'Festival', 449, 20, 400,
                m('Rasaganga Spl Thali', 'Masala Puri', 'Gulab Jamun', 'Payasam'),
                'food5.jpg', 'festival-sweets-savouries-thali.jpg',
            ),
        ]
        for name, cat_name, price, min_g, max_g, items, source_image, upload_as in packages_data:
            package = CateringPackage.objects.create(
                category=categories[cat_name],
                name=name,
                description=(
                    f'{name} from The Rasaganga — 100% vegetarian, made fresh with authentic South Indian '
                    'recipes and served the way Bellandur has known and loved for years.'
                ),
                price_per_plate=price,
                min_guests=min_g,
                max_guests=max_g,
            )
            package.menu_items.set(items)
            _attach_image(package, 'image', source_image, upload_as)

        self.stdout.write(self.style.SUCCESS('The Rasaganga catering data seeded successfully.'))
