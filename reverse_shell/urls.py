from .views import *
from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'attackers', AttackerViewSet)
router.register(r'victims', VictimViewSet)

app_name = 'reverse_shell'
urlpatterns = [
    path('', HomeViewSet.as_view(), name='index'),
    url(r'^signup/', SignupView.as_view(), name='signup'),
    url(r'^api/', include(router.urls)),
]

