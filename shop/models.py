from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='URL-имя')
    position = models.PositiveIntegerField(default=0, verbose_name='Порядок (меньше = выше)')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['position', 'name']

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        related_name='products', verbose_name='Категория'
    )
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена (тенге)')
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='Фото')
    is_available = models.BooleanField(default=True, verbose_name='Доступен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлен')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['category', 'name']

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_PROCESSING = 'processing'
    STATUS_DONE = 'done'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_NEW, 'Новый'),
        (STATUS_PROCESSING, 'В обработке'),
        (STATUS_DONE, 'Выполнен'),
        (STATUS_CANCELLED, 'Отменён'),
    ]

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='orders', verbose_name='Товар'
    )
    customer_name = models.CharField(max_length=100, verbose_name='Имя клиента')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(blank=True, verbose_name='Email')
    address = models.TextField(verbose_name='Адрес доставки')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES,
        default=STATUS_NEW, verbose_name='Статус'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заказ #{self.pk} — {self.customer_name} ({self.product.name})'

    def total_price(self):
        return self.product.price * self.quantity
    total_price.short_description = 'Сумма (тенге)'