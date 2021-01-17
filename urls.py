from django.urls import path
from users import views
from django.conf.urls.static import static

app_name='users'

urlpatterns = [
    path('login/signup/', views.signup, name='signup'),
    path('',views.main, name='main'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('login/signup/welcome/',views.welcome, name="welcome"),
    path('2/', views.main2, name='main2'),
    path('2/mypage/', views.mypage, name='mypage'),
]
