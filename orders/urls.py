from django.urls import path
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from orders import views as order_views


# Initialize the router for the orders app.
router = DefaultRouter()
router.register(r'orders', order_views.OrderViewSet)


urlpatterns = [
    path('add-to-cart/', order_views.AddToCartView.as_view(), name='add-to-cart'),
    path('remove-from-cart/', order_views.RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('create-order/', order_views.CreateOrderView.as_view(), name='create-order'),
    # path('', include(router.urls)),
 
]
