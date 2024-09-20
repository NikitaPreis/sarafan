from api.permissions import CustomerShoppingCartAccess
from api.serializers import (CategoryAndSubcategorySerializer,
                             GetProductsInShoppingCartSerializer,
                             ProductSerializer, ShoppingCartSerializer)
from core import constants as const
from core.views import (add_product_to_shopping_cart,
                        get_customer_shopping_cart_with_products,
                        get_product_in_shopping_cart, get_product_or_404,
                        get_shopping_cart_total_price_and_amount,
                        remove_product_from_shopping_cart)
from products.models import Category, Product, ShoppingCart
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class CategoryAndSubcategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryAndSubcategorySerializer
    permission_classes = (permissions.AllowAny,)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None

    @action(methods=['post', 'patch', 'delete'], detail=True,
            permission_classes=(CustomerShoppingCartAccess,))
    def shopping_cart(self, request, pk=None):
        product = get_product_or_404(pk=pk)
        product_in_shopping_cart = get_product_in_shopping_cart(
            user=request.user, product=product
        )
        if request.method == 'POST':
            if product_in_shopping_cart.exists():
                return Response(
                    {'error': const.PRODUCT_HAS_ALREADY_BEEN_ADDED_TO_CART},
                    status=status.HTTP_400_BAD_REQUEST
                )
            add_product_to_shopping_cart(request.user, product)
            product_in_shopping_cart.update(
                amount=const.PRODUCTS_IN_SHOPPING_CART_DEAFAULT_COUNT
            )
            serializer = ProductSerializer(product)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        if request.method == 'PATCH':
            if product_in_shopping_cart.exists():
                serializer = ShoppingCartSerializer(
                    product, data=request.data, partial=True,
                    context={
                        'product_in_shopping_cart': product_in_shopping_cart
                    }
                )
                if serializer.is_valid():
                    serializer.save()
                    product_in_shopping_cart.update(
                        amount=serializer.validated_data['amount']
                    )
                    return Response(
                        serializer.data, status=status.HTTP_201_CREATED
                    )
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        if request.method == 'DELETE':
            if product_in_shopping_cart.exists():
                remove_product_from_shopping_cart(product_in_shopping_cart)
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'error': const.PRODUCT_WASNT_ADD_TO_SHOPPING_CART},
            status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False,
            permission_classes=(CustomerShoppingCartAccess,))
    def get_shopping_cart(self, request):
        customer_shopping_cart = get_customer_shopping_cart_with_products(
            request.user
        )
        total_amount_and_price = get_shopping_cart_total_price_and_amount(
            customer_shopping_cart
        )
        if customer_shopping_cart.exists():
            serializer = GetProductsInShoppingCartSerializer(
                customer_shopping_cart,
                context=total_amount_and_price
            )
            return Response(serializer.data)
        return Response(
            {'error': const.SHOPPING_CART_IS_EMPTY},
            status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['delete'], detail=False,
            permission_classes=(CustomerShoppingCartAccess,))
    def empty_shopping_cart(self, request):
        if request.method == 'DELETE':
            customer_shopping_cart = ShoppingCart.objects.filter(
                user=request.user
            )
            if customer_shopping_cart.exists():
                customer_shopping_cart.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'error': const.CANT_CLEAR_EMPTY_SHOPPING_CART},
                status=status.HTTP_400_BAD_REQUEST
            )
