from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    children = serializers.ListSerializer(child=serializers.SerializerMethodField(), read_only=False)

    class Meta:
        model = Category
        fields = '__all__'

    def get_children(self, instance):
        children = instance.children.all()
        if children:
            return CategorySerializer(children, many=True).data
        return None