from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from agenda.serializers import AgendamentoSerializer, PrestadorSerializer
from agenda.models import Agendamento
from rest_framework.decorators import api_view, permission_classes
from rest_framework import  generics, permissions
from rest_framework.response import Response
from datetime import datetime
from agenda.utils import get_horarios
from agenda.tasks import gerar_relatorio, envia_email_com_anexo
from django.http import HttpResponse
from django.contrib.auth.models import User


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

@api_view(http_method_names=["GET"])
@permission_classes([permissions.IsAdminUser])
def prestador_list(request):
    if request.query_params.get("formato") == "csv":
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="prestadores.csv"'},
        )
        result = gerar_relatorio.delay()
        return Response({"task_id" : result.task_id})
    else:
        obj = User.objects.all()
        serializer = PrestadorSerializer(obj, many=True)
        return Response(serializer.data)
    

@api_view(http_method_names=["GET"])
def listar_horarios(request):
    data = request.query_params.get("data")
    
    if not data:
        data = datetime.now().date
    else:
        data = datetime.fromisoformat(data)

    horarios_disponiveis = sorted(list(get_horarios(data)))

    return JsonResponse(horarios_disponiveis, safe=False)