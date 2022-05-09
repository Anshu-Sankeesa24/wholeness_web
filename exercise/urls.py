from django.urls import path
from exercise import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home',views.home,name='home'),
    path('signup',views.register,name='register'),
    path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    path('account',views.account,name='account'),
    path('login', views.login, name='login'),
    path('logout', views.Logout, name='logout'),


    path('workout',views.workout,name='workout'),
    path('exercise',views.exercise,name='exercise'),
    path('diseases',views.diseases,name='diseases'),
    path('profile',views.profile,name='profile'),
    path('settings',views.setting,name='setting'),
    path('food',views.food,name='Diet'),
    path("external",views.external,name="external"),
    path("vlunch",views.veglunch,name='veg'),
    path("nvlunch",views.nonveglunch,name="non veg"),
    path("vbled",views.veg,name="veg"),
    path("nvbled",views.non_veg,name="non veg"),


    path('error',views.error,name='error'),
    path('success',views.success,name='success'),

]