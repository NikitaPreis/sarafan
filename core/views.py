from django.db.models import Sum
from django.shortcuts import get_object_or_404
from products.models import Product, ShoppingCart


def get_product_or_404(pk):
    """Получить продукт или вернуть ошибку 404."""
    return get_object_or_404(Product.objects, pk=pk)


def get_product_in_shopping_cart(user, product):
    """Проверить был ли продукт добавлен в корзину ранее."""
    return ShoppingCart.objects.filter(user=user, product=product)


def add_product_to_shopping_cart(user, product):
    """Добавить товар в продуктовую корзину."""
    return ShoppingCart.objects.create(user=user, product=product)


def remove_product_from_shopping_cart(product_in_shopping_cart):
    """Удалить товар из продутовой корзины."""
    return product_in_shopping_cart.delete()


def get_customer_shopping_cart_with_products(customer):
    """Получить корзину пользователя с товарами."""
    return ShoppingCart.objects.select_related('product').filter(user=customer)


def get_customer_shopping_cart_total_amount(customer_shopping_cart):
    """Получить общее количество товаров в корзине покупателя."""
    total_amount = customer_shopping_cart.aggregate(
        total_amount=Sum('amount', default=None)
    )
    return total_amount


def get_customer_shopping_cart_total_price(
        customer_shopping_cart,
        total_amount):
    """Получить общую цену товаров в корзине покупателя."""
    total_amount['total_price'] = 0
    for shopping_cart_obj in customer_shopping_cart:
        total_amount['total_price'] += (shopping_cart_obj.amount
                                        * shopping_cart_obj.product.price)
    return total_amount


def get_shopping_cart_total_price_and_amount(customer_shopping_cart):
    """Получить общую цену и количество товаров в корзине покупателя."""
    total_amount = get_customer_shopping_cart_total_amount(
        customer_shopping_cart
    )
    total_amount_and_price = get_customer_shopping_cart_total_price(
        customer_shopping_cart, total_amount
    )
    return total_amount_and_price
