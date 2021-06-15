"""R5_SHOP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from shop import view_sets

rest_router = routers.DefaultRouter()
rest_router.register(r'products', view_sets.ProductViewSet)
rest_router.register(r'announcements', view_sets.AnnouncementViewSet)
rest_router.register(r'users', view_sets.UserViewSet)
rest_router.register(r'buyer-show', view_sets.BuyerShowViewSet)
rest_router.register(r'shipping-address', view_sets.ShippingAddressViewSet)
rest_router.register(r'order', view_sets.OrderViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),  # for admin panel
    path('api/', include(rest_router.urls)),  # for restful api endpoint
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),  # for web restful client login
    path('api-token-auth/', obtain_auth_token)  # for restful client get api token, post {username, password}
]
