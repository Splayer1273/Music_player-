from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import path

app_name = "App"
urlpatterns = [
    path("index/",views.index,name="index"),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_song/', views.add_song, name='add_song'),
    path('about_us/', views.about_us, name='about_us')

]
