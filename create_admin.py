import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'metal_order_back.settings')

import django
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@vkusnyashki.kg', 'admin123')
    print('Суперпользователь создан: admin / admin123')
else:
    print('Суперпользователь admin уже существует')
