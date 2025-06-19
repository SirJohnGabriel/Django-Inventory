from django.urls import path
from . import views

app_name = "authuserapp"
urlpatterns = [
    path('', views.index, name='authhome'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),
]