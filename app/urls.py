from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index),
    path('about/', views.about),
    path('product/', views.product),
    path('testimonial/', views.testimonial),
    path('why/', views.why),
    path('signup', views.handleSignup),
    path('login', views.handlelogin),
    path('logout', views.handlelogout),
    path('search', views.search),
    path('product/<int:uid>', views.viewProduct),
]