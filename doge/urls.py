from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name="index"),
  path('register/', views.register, name="register"),
  path('logout/', views.logout_view, name="logout"),
  path('create/', views.create, name="create"),
  path('api/<str:function>/', views.api, name="api"),
  path('l/<str:id>', views.url_redirect, name="redirect"),
  path('dashboard/', views.dashboard, name="dashboard"),
  path('help/', views.help, name="help")
]