from django.urls import path
from agenda.views import AgendamentoDetail, AgendamentoList, prestador_list, listar_horarios

urlpatterns = [
    path('agendamentos/', AgendamentoList.as_view()),
    path('agendamentos/<int:pk>/', AgendamentoDetail.as_view()),
    path('prestadores/', prestador_list),
    path('horarios/', listar_horarios)
]
