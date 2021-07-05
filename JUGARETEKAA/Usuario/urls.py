from django.urls import path
from . import views

app_name = "usuario"
urlpatterns = [
    #leave empty string for base url
    path('login/', views.loginpage, name="login"),
    path('logout/', views.logoutpage, name="logout"),
    path('registro/', views.registro, name="registro"),    
]