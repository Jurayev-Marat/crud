from django.urls import path
from . import views

urlpatterns = [
    # BOSH SAHIFA
    path('', views.index, name='home'),

    # CATEGORY
    path('category/<int:pk>/', views.category, name='category'),

    # ADD URLlari
    path('add_category/', views.add_category, name='add_category'),
    path('add_product/', views.add_product, name='add_product'),
    path('add_suppliers/', views.add_suppliers, name='add_suppliers'),
    path('add_order_details/', views.add_order_details, name='add_order_details'),
    path('add_orders/', views.add_orders, name='add_orders'),

    # DELETE URLlari
    path('delete_category/<int:pk>/', views.delete_category, name='delete_category'),
    path('delete_product/<int:pk>/', views.delete_product, name='delete_product'),
    path('delete_supplier/<int:pk>/', views.delete_supplier, name='delete_supplier'),
    path('delete_order_detail/<int:pk>/', views.delete_order_detail, name='delete_order_detail'),
    path('delete_order/<int:pk>/', views.delete_order, name='delete_order'),

    # UPDATE URLlari
    path('update_category/<int:pk>/', views.update_category, name='update_category'),
    path('update_product/<int:pk>/', views.update_product, name='update_product'),
    path('update_supplier/<int:pk>/', views.update_supplier, name='update_supplier'),
    path('update_order_detail/<int:pk>/', views.update_order_detail, name='update_order_detail'),
    path('update_order/<int:pk>/', views.update_order, name='update_order'),
]