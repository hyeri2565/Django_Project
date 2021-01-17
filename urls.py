from django.urls import path
from Register_team import views
from django.urls import include

app_name = "Register_team"

urlpatterns = [
    path('', views.register, name="register"),
    path('complete/', views.register_complete, name="register_complete"),
]
