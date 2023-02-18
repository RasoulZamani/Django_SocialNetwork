from django.urls import path
from . import views

urlpatterns = [
    #path('', views.AccountView.as_view(), name='accounts'),
    path('register/', views.RegisterView.as_view(), name='user_register'),
]
