from django.urls import path
from products.views import ProductListView, ProductDetailView, CategoryListView, CategoryDetailView, FileListView, \
    FileDetailView , product_list ,product_detail ,category_list , product_list_by_category,contact_us,about_us,profile_view

urlpatterns = [
    #API urls
    path('products/',ProductListView.as_view(),name='product_list'),
    path('products/<int:pk>/',ProductDetailView.as_view(),name='product_detail'),
    path('categories/',CategoryListView.as_view(),name='category_list'),
    path('categories/<int:pk>/',CategoryDetailView.as_view(),name='category_detail'),
    path('products/<int:pk>/files/',FileListView.as_view(),name='file_list'),
    path('products/<int:product_pk>/files/<int:pk>/', FileDetailView.as_view(), name='file_detail'),

    #Front urls
    path('site/products/',product_list,name='product_list_frontend'),
    path('site/products/<int:pk>/',product_detail,name='product_detail_frontend'),
    path('', category_list, name='home'),
    path('site/categories/',category_list,name='category_list_frontend'),
    path('site/products/category/<int:category_id>/', product_list_by_category, name='product_list_by_category'),
    path('contact_us/',contact_us,name='contact_us'),
    path('about_us/',about_us,name='about_us'),
    path('profile/',profile_view,name='profile_page'),
]