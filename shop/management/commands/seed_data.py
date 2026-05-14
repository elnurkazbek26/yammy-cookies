from django.core.management.base import BaseCommand
from shop.models import Category, Product


CATEGORIES = [
    {'name': 'Пироги', 'slug': 'pies'},
    {'name': 'Торты', 'slug': 'cakes'},
    {'name': 'Кексы и маффины', 'slug': 'muffins'},
]

PRODUCTS = [
    # Пироги
    {
        'category_slug': 'pies',
        'name': 'Пирог с яблоком и корицей',
        'description': 'Нежный домашний пирог с сочными яблоками и ароматной корицей. Хрустящее тесто снаружи, мягкая начинка внутри. Идеален к чаю и кофе.',
        'price': 450,
    },
    {
        'category_slug': 'pies',
        'name': 'Пирог с вишней',
        'description': 'Сладко-кислая вишнёвая начинка в нежной слоёной оболочке. Классика домашней выпечки, которую обожают дети и взрослые.',
        'price': 480,
    },
    {
        'category_slug': 'pies',
        'name': 'Пирог с мясом и луком',
        'description': 'Сытный и ароматный пирог из дрожжевого теста с сочной мясной начинкой. Идеально подходит как основное блюдо или к праздничному столу.',
        'price': 550,
    },
    {
        'category_slug': 'pies',
        'name': 'Медовый пирог',
        'description': 'Воздушный пирог с натуральным мёдом и орехами. Тонкие медовые коржи, пропитанные нежным кремом — настоящее удовольствие.',
        'price': 520,
    },
    # Торты
    {
        'category_slug': 'cakes',
        'name': 'Торт "Наполеон"',
        'description': 'Легендарный торт из тончайших хрустящих коржей с нежным заварным кремом. Готовится по классическому рецепту, настаивается ночь для идеального вкуса.',
        'price': 1200,
    },
    {
        'category_slug': 'cakes',
        'name': 'Торт "Медовик"',
        'description': 'Многослойный медовый торт с мягкими пропитанными коржами и воздушной сметанной прослойкой. Нежный вкус детства в каждом кусочке.',
        'price': 1100,
    },
    {
        'category_slug': 'cakes',
        'name': 'Шоколадный торт "Брауни"',
        'description': 'Насыщенный шоколадный торт с тёмным бельгийским шоколадом. Влажный и плотный, с хрустящей корочкой — мечта любого шокоголика.',
        'price': 1350,
    },
    {
        'category_slug': 'cakes',
        'name': 'Торт "Чёрный лес"',
        'description': 'Немецкая классика: шоколадные бисквитные коржи, вишня, взбитые сливки и шоколадная стружка. Элегантный и изысканный десерт.',
        'price': 1400,
    },
    # Кексы
    {
        'category_slug': 'muffins',
        'name': 'Маффины с черникой',
        'description': 'Нежные маффины, наполненные свежей черникой. Мягкие внутри, с лёгкой золотистой корочкой. Отличный завтрак или перекус.',
        'price': 80,
    },
    {
        'category_slug': 'muffins',
        'name': 'Шоколадные маффины',
        'description': 'Пышные шоколадные маффины с кусочками шоколада внутри. Каждый — маленькое счастье для сладкоежки.',
        'price': 90,
    },
    {
        'category_slug': 'muffins',
        'name': 'Кекс лимонный',
        'description': 'Освежающий лимонный кекс с цедрой и лимонной глазурью. Идеальный баланс сладкого и кислого, лёгкий и ароматный.',
        'price': 350,
    },
]


class Command(BaseCommand):
    help = 'Заполнить базу данных тестовыми категориями и товарами'

    def handle(self, *args, **options):
        self.stdout.write('Создаю категории...')
        categories = {}
        for cat_data in CATEGORIES:
            cat, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name']}
            )
            categories[cat_data['slug']] = cat
            status = 'создана' if created else 'уже есть'
            self.stdout.write(f'  [{status}] {cat.name}')

        self.stdout.write('Создаю товары...')
        for prod_data in PRODUCTS:
            category = categories[prod_data['category_slug']]
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults={
                    'category': category,
                    'description': prod_data['description'],
                    'price': prod_data['price'],
                    'is_available': True,
                }
            )
            status = 'создан' if created else 'уже есть'
            self.stdout.write(f'  [{status}] {product.name} — {product.price} сом')

        self.stdout.write(self.style.SUCCESS('\nГотово! Все данные загружены.'))
        self.stdout.write('Откройте http://127.0.0.1:8000/ чтобы увидеть каталог.')
        self.stdout.write('Админка: http://127.0.0.1:8000/admin/')
