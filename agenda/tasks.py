import csv
from io import StringIO
from agenda.serializers import PrestadorSerializer
from django.contrib.auth.models import User
from tamarcado.celery import app

@app.task
def gera_relatorio_prestadores():
    output =StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "prestador",
        "data_horario",
        "nome_cliente",
        "email_cliente",
        "cancelado"
    ])
    obj = User.objects.all()
    serializer = PrestadorSerializer(obj, many=True)
    for prestador in serializer.data:
        agendamentos = prestador["agendamentos"]
        for agendamento in agendamentos:
            writer.writerow([
                agendamento['prestador'],
                agendamento['data_horario'],
                agendamento['nome_cliente'],
                agendamento['email_cliente'],
                agendamento["cancelado"],
            ])