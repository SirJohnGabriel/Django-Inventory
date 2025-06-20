from django.urls import path
from . import views

app_name = "authuserapp"
urlpatterns = [
    path('', views.index, name='authhome'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('register', views.register, name='register'),
    # path('inventory/', views.inventory, name='inventory'),

    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/add/', views.inventory_create, name='inventory_add'),
    path('inventory/<int:pk>/edit/', views.inventory_update, name='inventory_edit'),
    path('inventory/<int:pk>/delete/', views.inventory_delete, name='inventory_delete'),
]