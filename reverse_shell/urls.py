from .views import *
from django.urls import path
from django.conf.urls import url

app_name = 'reverse_shell'
urlpatterns = [
    path('', HomeViewSet.as_view(), name='index'),
    url(r'^register/', RegisterView.as_view(), name='signup'),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^validate-login', ValidateLoginView.as_view(), name='validate_login'),
    path('choose-victim/', VictimsView.as_view(), name='choose_victim'),
    path('attack/', AttackView.as_view(), name='attack'),
]
