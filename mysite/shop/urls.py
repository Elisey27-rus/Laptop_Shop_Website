from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views
from .views import (main_page,
                    create,
                    product_category_page,
                    ProductDetailsView,
                    start_page,
                    login_view,
                    LogoutView,
                    create_profile,
                    profile_view,
                    RegisterView,
                    view_cart,
                    )

app_name = 'shop'

urlpatterns = [
    path('main_page/', main_page, name='main_page'),
    path('create/<slug:value>/', create, name='create'),
    path('category/<slug:value>/', product_category_page, name='product_category_page'),
    path('products/<int:pk>/', ProductDetailsView.as_view(), name="product_details"),
    path('', start_page, name='start_page'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('create_profile/', create_profile, name='create_profile'),
    path('registration/', RegisterView.as_view(), name='registration'),
    path('cart/', view_cart, name='view_cart')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
