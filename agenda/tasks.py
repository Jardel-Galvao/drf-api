import csv
from io import StringIO
from agenda.serializers import PrestadorSerializer
from django.contrib.auth.models import User
from tamarcado.celery import app
from django.core.mail import EmailMessage

@app.task
def gerar_relatorio() -> StringIO:
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
    envia_email_com_anexo(output)

@app.task
def envia_email_com_anexo(anexo):
    email = EmailMessage(
        'tamarcado-Relatório de prestadores',
        'Em anexo o relatório solicitado.',
        'jardelgalvao1@gmail.com',
        ['jardelgalvao1@gmail.com'],
    )

    email.attach("relatorio.csv", anexo.getvalue(), "text/csv")
    email.send()