from rest_framework.routers import DefaultRouter


from apps.user.views import UserViewSet
from apps.product import views as product_views
from apps.cart.views import CartViewSet
from apps.discount.views import DiscountViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'products', product_views.ProductViewSet, basename='product')
router.register(r'categories', product_views.CategoryViewSet, basename='category')
router.register(r'carts', CartViewSet, basename='cart')
router.register(r'discounts', DiscountViewSet, basename='discount')

urlpatterns = router.urls
