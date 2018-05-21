from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'plots'

# Enter all urls for website here
urlpatterns = [
    # path('', views.index, name='index'), # Delete this as it was default
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('mi1/', views.Mi1View.as_view(), name='mi1'),
    path('landscape/', views.LandscapeView.as_view(), name='landscape'),
]
