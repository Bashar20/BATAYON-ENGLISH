from django.urls import path
from accounts import views
urlpatterns = [
    path("", views.index,name="index"),
    path('register/', views.register, name='register'),
    path('userLogin/', views.userLogin, name='userLogin'),
]
