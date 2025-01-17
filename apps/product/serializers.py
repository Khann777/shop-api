from rest_framework import serializers

from .models import Product, ProductImage

from django.db.models import Avg

from ..review.serializers import CommentSerializer


class BaseProductSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    def get_discounted_price(self, instance):
        if instance.discount is not None:
            discounted_price = instance.price - (instance.price * instance.discount / 100)
            return discounted_price
        return None

    def get_average_rating(self, instance):
        return instance.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0.0

class ProductListSerializer(BaseProductSerializer):
    discounted_price = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'stock', 'average_rating']


class ProductDetailSerializer(BaseProductSerializer):
    discounted_price = serializers.SerializerMethodField()
    owner = serializers.ReadOnlyField(source='owner.email')
    product_images = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    def get_product_images(self, instance):
        product_images = instance.images.all()
        if product_images:
            return ProductImageSerializer(product_images, many=True).data
        return None

    def get_comments(self, instance):
        comments = instance.comments.all()
        if comments:
            return CommentSerializer(comments, many=True).data
        return None

    class Meta:
        model = Product
        fields = '__all__'

class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'title',
            'price',
            'description',
            'quantity',
            'discount',
            'category',
        ]

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'

