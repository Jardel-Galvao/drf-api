from django.shortcuts import get_object_or_404
from agenda.serializers import AgendamentoSerializer
from agenda.models import Agendamento
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins, generics
from datetime import datetime
class AgendamentoList(generics.ListCreateAPIView):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
class AgendamentoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
