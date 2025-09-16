from django.urls import path
from . import views


urlpatterns = [
    path('store/', views.shop, name="shop"),
    #TODO: Add more paths for shop detail, categories, cart, checkout, etc.
    path('shop-detail/',views.shop_detail,name='shop_detail')
]
