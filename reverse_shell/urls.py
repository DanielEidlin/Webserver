from .views import *
from django.conf.urls import url
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'reverse_shell'
urlpatterns = [
    path('', HomeViewSet.as_view(), name='index'),
    url(r'^register/', RegisterView.as_view(), name='signup'),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^validate-login', ValidateLoginView.as_view(), name='validate_login'),
    path('connect/<str:room_name>/', RoomView.as_view(), name='room'),
]
