from django.urls import path
from.import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('',views.index),
    path('about_us',views.display_aboutus_page),
    path('productlist/<int:id>',views.display_productlist),
    path('register_form',views.display_register_form),
    path('register', views.registeration),
    path('login', views.login),
    path('products/<int:id>', views.display_product),
    path('recommend',views.recommend_product),
    path('addreview', views.add_review),
    path('logout', views.logout),
    path('delete',views.delete),
    path('edit', views.edit),
    path('edit_review', views.edit_review),
    path('search', csrf_exempt(views.search_item)),
    path('submitRecommendation', views.submit_recommendation),
    path('thank-you', views.get_thanks_to_user)
    
    
]