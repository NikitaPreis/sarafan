from api.views import CategoryAndSubcategoryViewSet, ProductViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet

app_name = 'api'

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('categories', CategoryAndSubcategoryViewSet,
                basename='category')
router.register('products', ProductViewSet, basename='product')


urlpatterns = [
    path('', include(router.urls)),
]
