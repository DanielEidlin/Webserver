from .views import *
from django.conf.urls import url
from django.urls import path, include
from django.contrib.auth.views import LoginView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'attackers', AttackerViewSet)
router.register(r'victims', VictimViewSet)

app_name = 'reverse_shell'
urlpatterns = [
    path('', HomeViewSet.as_view(), name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^signup/', SignupView.as_view(), name='signup'),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^api/', include(router.urls)),
]
