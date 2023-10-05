from django.urls import path
from agenda.views import AgendamentoDetail, AgendamentoList, PrestadorList, listar_horarios

urlpatterns = [
    path('agendamentos/', AgendamentoList.as_view()),
    path('agendamentos/<int:pk>/', AgendamentoDetail.as_view()),
    path('prestadores/', PrestadorList.as_view()),
    path('horarios/', listar_horarios)
]
