import urllib.request
import urllib.error
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from shop.models import Product

# Для каждого товара — прямая ссылка на фото с Unsplash (стабильные ID)
PRODUCT_IMAGES = {
    'Пирог с яблоком и корицей': 'https://images.unsplash.com/photo-1562440499-64b9a86dd073?w=600&q=80',
    'Пирог с вишней':            'https://images.unsplash.com/photo-1528975604071-b4dc52a2d18c?w=600&q=80',
    'Пирог с мясом и луком':     'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&q=80',
    'Медовый пирог':             'https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=600&q=80',
    'Торт "Наполеон"':           'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=600&q=80',
    'Торт "Медовик"':            'https://images.unsplash.com/photo-1464349095431-e9a21285b5f3?w=600&q=80',
    'Шоколадный торт "Брауни"':  'https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=600&q=80',
    'Торт "Чёрный лес"':         'https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=600&q=80',
    'Маффины с черникой':        'https://images.unsplash.com/photo-1607958996333-41aef7caefaa?w=600&q=80',
    'Шоколадные маффины':        'https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=600&q=80',
    'Кекс лимонный':             'https://images.unsplash.com/photo-1551879400-111a9087cd86?w=600&q=80',
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}


class Command(BaseCommand):
    help = 'Скачать фото для товаров с Unsplash'

    def handle(self, *args, **options):
        for product in Product.objects.all():
            url = PRODUCT_IMAGES.get(product.name)
            if not url:
                self.stdout.write(f'  [пропуск] нет URL для «{product.name}»')
                continue

            if product.image:
                self.stdout.write(f'  [есть]   «{product.name}» — фото уже загружено')
                continue

            self.stdout.write(f'  Скачиваю «{product.name}»...')
            try:
                req = urllib.request.Request(url, headers=HEADERS)
                with urllib.request.urlopen(req, timeout=15) as resp:
                    content = resp.read()

                filename = f"{product.pk}_{product.name[:20].replace(' ', '_')}.jpg"
                product.image.save(filename, ContentFile(content), save=True)
                self.stdout.write(self.style.SUCCESS(f'  [OK]     «{product.name}»'))

            except (urllib.error.URLError, Exception) as e:
                self.stdout.write(self.style.ERROR(f'  [ошибка] «{product.name}»: {e}'))

        self.stdout.write('\nГотово!')
