from django.views import View
from django.urls import reverse_lazy
from .models import Attacker, Victim
from rest_framework.response import Response
from rest_framework.decorators import action
from django.views.generic.edit import FormView
from rest_framework import viewsets, permissions
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from .serializers import AttackerSerializer, VictimSerializer


class HomeViewSet(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'index.html')


class SignupView(FormView):
    template_name = 'registration/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('reverse_shell:login')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.save()
        return super().form_valid(form)


class AttackerViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing attackers.
    """
    queryset = Attacker.objects.all()
    serializer_class = AttackerSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def get_attacker(self, request):
        """
        Returns all the attacker who requested to connect to this victim.
        :return: Serialized attacker that requested to connect to this victim.
        """
        mac_address = request.query_params['mac_address']
        attacker = get_object_or_404(Attacker, victim__mac_address=mac_address)
        serialized_attacker = AttackerSerializer(attacker, many=False)
        return Response(serialized_attacker.data)


class VictimViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing victims.
    """
    queryset = Victim.objects.all()
    serializer_class = VictimSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def available_victims(self):
        """
        Returns all the logged in victims.
        :return: Serialized victims that are logged in.
        """
        available_victims = Victim.objects.filter(logged_in=True)
        serialized_victims = VictimSerializer(available_victims, many=True)
        return Response(serialized_victims.data)
