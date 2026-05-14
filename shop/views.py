from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, Order
from .forms import OrderForm


def catalog(request):
    categories = Category.objects.prefetch_related('products').all()
    return render(request, 'shop/catalog.html', {
        'categories': categories,
        'total_products': Product.objects.filter(is_available=True).count(),
        'total_categories': Category.objects.count(),
        'total_orders': Order.objects.filter(status=Order.STATUS_DONE).count(),
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_available=True)
    form = OrderForm()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            order.save()
            return redirect('order_success', pk=order.pk)

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'form': form,
    })


def order_success(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'shop/order_success.html', {'order': order})
