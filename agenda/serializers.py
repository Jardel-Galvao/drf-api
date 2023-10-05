from rest_framework import serializers
from agenda.models import Agendamento
from django.utils import timezone
from django.contrib.auth.models import User

class AgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        fields = "__all__"

    prestador = serializers.CharField()

    def validate_prestador(self, value):
        try:
            obj_prestador = User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Usuário não existe!")
        return obj_prestador

    def validate_data_horario(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Agendamento não pode ser feito no passado!")
        if Agendamento.objects.filter(data_horario=value).exists():
            raise serializers.ValidationError("Esse horário não está disponível")
        return value
    
    def validate(self, attrs):
        
        email_cliente = attrs.get("email_cliente", "")
        telefone_cliente = attrs.get("telefone_cliente", "")

        if email_cliente.endswith(".br") and telefone_cliente.startswith("+") and not telefone_cliente.startswith("+55"):
            raise serializers.ValidationError("Email brasileito deve estar associado a um número do Brasil (+55)")
        return attrs

class PrestadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "agendamentos"]

    agendamentos = AgendamentoSerializer(many=True, read_only=True)