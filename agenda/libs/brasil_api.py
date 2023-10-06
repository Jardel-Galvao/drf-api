from datetime import date
import requests
from django.conf import settings

def is_feriado(data:date) -> bool:
    if settings.TESTING == True:
        if data.day == 25 and data.month ==12:
            return True
        return False
    
    request =  requests.get(f"https://brasilapi.com.br/api/feriados/v1/{data.year}")

    if request.status_code != 200:
        raise ValueError("Não foi possível consultar os feriados!")
    
    for feriado in request.json():
        if feriado['date'] == str(data.date()):
            return True

    return False