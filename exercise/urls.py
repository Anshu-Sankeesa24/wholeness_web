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
    path('pushups',views.pushup,name='pushups'),
    path("planks",views.planks,name="planks"),
    path('diseases',views.diseases,name='diseases'),
    path('profile',views.profile,name='profile'),
    path('settings',views.setting,name='setting'),
    path('profile_main',views.main_view,name='main_graph'),
    path('graph',views.graph,name='graph'),
    path('food',views.food,name='Diet'),
    path("externalpushup",views.external_pushups,name="external"),
    path("externalplank",views.external_planks,name="external"),
    path("vlunch",views.veglunch,name='veg'),
    path("nvlunch",views.nonveglunch,name="non veg"),
    path("nvbreakfast",views.nonvegbreak,name="non veg"),
    path("nvdinner",views.nonvegdinner,name="non veg"),
    path("nvevng",views.nonvegsnacks,name="non veg"),
    path("vbled",views.veg,name="veg"),
    path("nvbled",views.non_veg,name="non veg"),


    path("bladder",views.bladder,name='bladder'),
    path("digestive",views.digestive,name='bladder'),
    path("femalerep",views.femrep,name='bladder'),
    path("heart",views.heart,name='bladder'),
    path("kidney",views.kidney,name='bladder'),
    path("liver",views.liver,name='bladder'),
    path("malerep",views.malrep,name='bladder'),
    path("pancreases",views.pancreases,name='bladder'),
    path("respiratory",views.respiratory,name='bladder'),


    path('error',views.error,name='error'),
    path('success',views.success,name='success'),

]