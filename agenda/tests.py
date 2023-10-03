from rest_framework.test import APITestCase
import json
from datetime import datetime, timezone
from agenda.models import Agendamento

class TestListagemAgendamentos(APITestCase):
    def test_listagem_vazia(self):
        response = self.client.get("/api/agendamentos/")
        data = json.loads(response.content)
        self.assertEqual(data, [])
    
    def test_listagem_de_agendamentos_criados(self):
        Agendamento.objects.create(
            data_horario=datetime(2099,3,15,17,30, tzinfo=timezone.utc),
            nome_cliente = "Teste",
            email_cliente = "teste@teste.com",
            telefone_cliente = "4899999999",
        )

        Agendamento_serializado = {
            "id" : 1,
            "data_horario": "2099-03-15T17:30:00Z",
            "nome_cliente" : "Teste",
            "email_cliente" : "teste@teste.com",
            "telefone_cliente" : "4899999999",
        }

        response = self.client.get("/api/agendamentos/")
        data = json.loads(response.content)
        self.assertDictEqual(data[0], Agendamento_serializado)
    
class TestCriacaoAgendamento(APITestCase):
    def test_cria_agendamento(self):
        data =  {
            "data_horario": datetime(2099, 5, 1),
            "nome_cliente" : "Teste",
            "email_cliente" : "teste@teste.com",
            "telefone_cliente" : "4899999999",
        }

        Agendamento_serializado = {
            "id" : 1,
            "data_horario": "2099-05-01T00:00:00Z",
            "nome_cliente" : "Teste",
            "email_cliente" : "teste@teste.com",
            "telefone_cliente" : "4899999999",
        }

        response_post = self.client.post("/api/agendamentos/", data, format='json')
        response_get = self.client.get("/api/agendamentos/")
        data = json.loads(response_get.content)

        self.assertEqual(data[0], Agendamento_serializado)
    
    def test_quando_request_e_invalido_retorna_400(self):
        data = {
            "nome_cliente" : "Teste",
            "email_cliente" : "teste@teste.com",
            "telefone_cliente" : "4899999999",
        }
        response = self.client.post("/api/agendamentos/", data, format='json')
        self.assertEqual(response.status_code, 400)

class TestDetalharAgendamento(APITestCase):
    def test_detalhar_agendamento(self):
        data = {
                "data_horario": datetime(2099, 5, 1),
                "nome_cliente" : "Teste",
                "email_cliente" : "teste@teste.com",
                "telefone_cliente" : "4899999999",
        }

        Agendamento_serializado = {
            "id" : 1,
            "data_horario": "2099-05-01T00:00:00Z",
            "nome_cliente" : "Teste",
            "email_cliente" : "teste@teste.com",
            "telefone_cliente" : "4899999999",
        }
        response_post = self.client.post("/api/agendamentos/", data, format='json')
        response_get = self.client.get("/api/agendamentos/1/")
        data = json.loads(response_get.content)
        self.assertDictEqual(data, Agendamento_serializado)

    def test_editar_agendamento(self):
        data = {
               "data_horario": datetime(2099, 5, 1),
               "nome_cliente" : "Teste",
               "email_cliente" : "teste@teste.com",
               "telefone_cliente" : "4899999999",
        }
        edicao_agendamento = {"nome_cliente" : "Teste2"}
        Agendamento_serializado = {
            "id" : 1,
            "data_horario": "2099-05-01T00:00:00Z",
            "nome_cliente" : "Teste2",
            "email_cliente" : "teste@teste.com",
            "telefone_cliente" : "4899999999",
        }
        response_post = self.client.post("/api/agendamentos/", data, format='json')
        response_patch = self.client.patch("/api/agendamentos/1/", edicao_agendamento, format='json')
        response_get = self.client.get("/api/agendamentos/1/")
        data = json.loads(response_get.content)
        self.assertDictEqual(data, Agendamento_serializado)
    
    def test_cancelar_agendamento(self):
        data = {
            "data_horario": datetime(2099, 5, 1),
            "nome_cliente" : "Teste",
            "email_cliente" : "teste@teste.com",
            "telefone_cliente" : "4899999999",
        }
        response_post = self.client.post("/api/agendamentos/", data, format='json')
        response_delete = self.client.patch("/api/agendamentos/1/")
        obj = Agendamento.objects.get()
        obj.cancelado = True
        obj.save()

        self.assertEqual(obj.cancelado, True)
