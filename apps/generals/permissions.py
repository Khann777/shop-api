from rest_framework.permissions import BasePermission

from apps.product.models import Product

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Проверяем, аутентифицирован ли пользователь
        if not request.user.is_authenticated:
            return False
        # Сравниваем пользователя с владельцем объекта
        return request.user == obj.owner

class IsProductOwner(BasePermission):
    def has_permission(self, request, view):
        print(request)
        if request.user or not request.user.is_authenticated:
            return False
        product_id = view.kwargs.get('pk')

        try:
            product = Product.objects.get(id=product_id)
            return product.owner == request.user
        except Product.DoesNotExist:
            return False
