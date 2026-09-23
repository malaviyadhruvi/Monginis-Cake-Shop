"""
URL configuration for monginis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from monginis import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from .views import chatbot_response

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('product.html',views.product,name='product'),
    path('about.html',views.about,name='about_html'),
    path('blog.html', views.blog, name='blog_html'),
 #   path('cake.html', views.cake, name='cake'),
    path('pastry.html', views.pastry_list, name='pastry_list'),
    path('package.html', views.packaged_cake_list, name='packaged_cake_list'),
    path('donuts.html', views.donuts_list, name='donuts_list'),
    path('muffins.html', views.muffin_list, name='muffin_list'),
    path('brownie.html', views.brownie_list, name='brownie_list'),
    path('choco.html', views.chocolate_list, name='chocolate_list'),
    path('chocolate_bouquet.html', views.chocolate_bouquet_list, name='chocolate_bouquet_list'),
    path('history.html', views.history, name='history'),
    path('categories/', views.category_list, name='category_list'),
    path('header.html', views.header, name='header'),
    path('header1.html', views.header1, name='header1'),
    path('footer.html', views.footer, name='foooter'),
    path('order.html', views.order, name='order'),
    path("login/", views.user_login, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('payment/', views.payment, name='payment'),
    path('order_successful/', views.order_successful, name='order_successful'),
    path('cart.html',views.cart,name='cart'),
    path('success.html', views.success, name='success'),
    path('registration.html', views.registration, name='registration'),
    path('profile.html', views.profile_view, name='profile'),
    path('cake/',views.cake_list,name='cake_list'),
    path('order/', views.order_view, name='order'),
    path('orderpage/',views.orderpage_view,name='orderpage_view'),
    path('cart_view/', views.cart_view, name='cart_view'),
    path('visit/', views.visit, name='visit'),
    path('forgot_password.html', views.forgot_password_view, name='forgot_password_view'), 
    path('chatbot/get-response/', chatbot_response, name='chatbot_response'),
    path('download-invoice/<int:order_id>/', views.download_invoice, name='download_invoice'),
   
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)