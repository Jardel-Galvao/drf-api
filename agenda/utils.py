from datetime import datetime, timedelta, timezone, date
from typing import Iterable
from agenda.models import Agendamento
from agenda.libs.brasil_api import is_feriado

def get_horarios(data: date) -> Iterable[datetime]:

    if is_feriado(data) == True:
        return []
    
    inicio = datetime(year=data.year, month=data.month, day=data.day, hour=9, minute=0, tzinfo=timezone.utc)
    fim = datetime(year=data.year, month=data.month, day=data.day, hour=19, minute=0, tzinfo=timezone.utc)
    intervalo_entre_horas = timedelta(minutes=30)

    horarios_disponiveis = set()

    while inicio <= fim:
        if not Agendamento.objects.filter(data_horario=inicio).exists():
            horarios_disponiveis.add(inicio)
        inicio = inicio + intervalo_entre_horas

    return horarios_disponiveis