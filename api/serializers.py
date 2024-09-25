import base64

from core import constants as const
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from products.models import (Category, Product, ProductImagesDesktop,
                             ShoppingCart, Subcategory)
from rest_framework import serializers

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ('id', 'name', 'slug', 'image')
        read_only_fields = ('id', 'name', 'slug',
                            'image')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'image')


class CategoryAndSubcategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(read_only=True, many=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug',
                  'image', 'subcategories')


class ShoppingCartSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='product.id'
    )
    name = serializers.StringRelatedField(
        read_only=True,
        source='product.name'
    )
    slug = serializers.StringRelatedField(
        read_only=True,
        source='product.slug'
    )

    class Meta:
        model = ShoppingCart
        fields = ('id', 'name', 'slug', 'amount')


class ProductImagesSerializer(serializers.ModelSerializer):
    image_detail = serializers.ImageField(read_only=True)
    image_list = serializers.ImageField(read_only=True)
    image_thumbnail = serializers.ImageField(read_only=True)

    class Meta:
        model = ProductImagesDesktop
        fields = ('image_detail', 'image_list', 'image_thumbnail')


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    subcategory = SubcategorySerializer(read_only=True)
    images = ProductImagesSerializer(read_only=True, many=True,
                                     source='product_images_desktop')

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug',
                  'category', 'subcategory',
                  'price', 'images')


class ImageThumbnailRelatedField(serializers.RelatedField):
    def to_representation(self, instance):
        url = instance.image_thumbnail.url
        request = self.context.get('request', None)
        if request is not None:
            return request.build_absolute_uri(url)
        return url


class GetShoppingCartSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='product.id'
    )
    name = serializers.StringRelatedField(
        read_only=True,
        source='product.name'
    )
    slug = serializers.StringRelatedField(
        read_only=True,
        source='product.slug'
    )
    price = serializers.StringRelatedField(
        read_only=True,
        source='product.price'
    )
    image = ImageThumbnailRelatedField(
        read_only=True,
        many=True,
        allow_null=True,
        source='product.product_images_desktop'
    )

    class Meta:
        model = ShoppingCart
        fields = ('id', 'name', 'slug',
                  'amount', 'price', 'image')


class ProductAndAmountSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )
    name = serializers.StringRelatedField(
        read_only=True,
        source='product.name',
    )
    slug = serializers.StringRelatedField(
        read_only=True,
        source='product.slug'
    )

    class Meta:
        model = ShoppingCart
        fields = ('id', 'name', 'slug', 'amount')


class GetProductsInShoppingCartSerializer(serializers.ModelSerializer):

    products = GetShoppingCartSerializer(read_only=True,
                                         many=True,
                                         source='*')
    total_amount = serializers.SerializerMethodField(
        read_only=True,
        default=const.DEFAULT_TOTAL_COUNT_VALUE_IN_SHOPPING_CART
    )
    total_price = serializers.SerializerMethodField(
        read_only=True, default=const.DEFAULT_TOTAL_SUM_VALUE_IN_SHOPPING_CART
    )

    class Meta:
        model = ShoppingCart
        fields = ('products', 'total_price', 'total_amount')

    def get_total_amount(self, obj):
        return self.context['total_amount']

    def get_total_price(self, obj):
        return self.context['total_price']

    def validate_total_amount(self, value):
        if value < const.PRODUCTS_IN_SHOPPING_CART_MIN_COUNT:
            raise serializers.ValidationError(
                const.PRODUCTS_IN_SHOPPING_CART_MIN_COUNT_ERROR
            )
        return value

    def validate_total_price(self, value):
        if value < const.PRODUCTS_IN_SHOPPING_CART_MIN_SUM:
            raise serializers.ValidationError(
                const.PRODUCTS_IN_SHOPPING_CART_MIN_SUM_ERROR
            )
        return value
