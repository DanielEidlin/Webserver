from .views import *
from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth.views import LoginView, LogoutView

router = DefaultRouter()
router.register(r'attackers', AttackerViewSet)
router.register(r'victims', VictimViewSet)
router.register(r'users', UserViewSet)

app_name = 'reverse_shell'
urlpatterns = [
    path('', HomeViewSet.as_view(), name='index'),
    url(r'^register/', RegisterView.as_view(), name='signup'),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^validate-login', ValidateLoginView.as_view(), name='validate_login'),
    url(r'^api/', include(router.urls)),
]
