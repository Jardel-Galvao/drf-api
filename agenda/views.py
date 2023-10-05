from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from agenda.serializers import AgendamentoSerializer, PrestadorSerializer
from agenda.models import Agendamento
from rest_framework.decorators import api_view
from rest_framework import  generics, permissions
from django.contrib.auth.models import User
from datetime import datetime
from agenda.utils import get_horarios
import requests



class IsOwnerOrCreateOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        username = request.query_params.get("username", None)
        if request.user.username == username:
            return True
        return False

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.prestador:
            return True
        else:
            return False

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff == True:
            return True
        else:
            return False
    
class AgendamentoList(generics.ListCreateAPIView):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
    permission_classes = [IsOwnerOrCreateOnly]

    def get_queryset(self):
        username = self.request.query_params.get("username", None)
        queryset = Agendamento.objects.filter(prestador__username=username)
        return queryset
    
class AgendamentoDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwner]
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer

class PrestadorList(generics.ListAPIView):
    serializer_class = PrestadorSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]


@api_view(http_method_names=["GET"])
def listar_horarios(request):
    data = request.query_params.get("data")
    
    if not data:
        data = datetime.now().date
    else:
        data = datetime.fromisoformat(data)

    horarios_disponiveis = sorted(list(get_horarios(data)))

    if horarios_disponiveis == []:
        return JsonResponse({"erro" : "Não é possível agendar em um feriado"})
    else:
        return JsonResponse(horarios_disponiveis, safe=False)