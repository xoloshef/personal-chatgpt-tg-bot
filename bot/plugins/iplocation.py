# Библиотека для HTTP-запросов к API
import requests
# Тип Dict для аннотаций
from typing import Dict

# Базовый класс плагина, от которого наследуемся
from .plugin import Plugin


# Класс плагина геолокации по IP-адресу
class IpLocationPlugin(Plugin):
    """
    A plugin to get geolocation and other information for a given IP address
    """

    # Возвращает имя источника данных для отображения в ответе
    def get_source_name(self) -> str:
        return "IP.FM"

    # Описание функции для OpenAI — модель вызывает её при вопросах об IP
    def get_spec(self) -> [Dict]:
        return [{
            # Имя функции, которое видит модель
            "name": "iplocation",
            # Описание — когда модель должна вызывать эту функцию
            "description": "Get information for an IP address using the IP.FM API.",
            # Схема параметров в формате JSON Schema
            "parameters": {
                "type": "object",
                "properties": {
                    # Единственный параметр — IP-адрес
                    "ip": {"type": "string", "description": "IP Address"}
                },
                # Параметр обязателен
                "required": ["ip"],
            },
        }]
        
    # Выполнение запроса к API при вызове функции моделью
    async def execute(self, function_name, helper, **kwargs) -> Dict:
        # Получаем IP из аргументов, переданных моделью
        ip = kwargs.get('ip')
        # Шаблон URL API IP.FM
        BASE_URL = "https://api.ip.fm/?ip={}"
        # Подставляем IP в URL
        url = BASE_URL.format(ip)
        try:
            # Отправляем GET-запрос к API
            response = requests.get(url)
            # Парсим JSON-ответ
            response_data = response.json()
            # Извлекаем страну (или "None" при отсутствии)
            country = response_data.get('data', {}).get('country', "None")
            # Регион/область
            subdivisions = response_data.get('data', {}).get('subdivisions', "None")
            # Город
            city = response_data.get('data', {}).get('city', "None")
            # Собираем строку локации, отфильтровывая пустые значения
            location = ', '.join(filter(None, [country, subdivisions, city])) or "None"
        
            # ASN — номер автономной системы (провайдер)
            asn = response_data.get('data', {}).get('asn', "None")
            # Название провайдера
            as_name = response_data.get('data', {}).get('as_name', "None")
            # Домен провайдера
            as_domain = response_data.get('data', {}).get('as_domain', "None")       
            # Возвращаем словарь с результатом для модели
            return {"Location": location, "ASN": asn, "AS Name": as_name, "AS Domain": as_domain}
        except Exception as e:
            # При любой ошибке возвращаем описание
            return {"Error": str(e)}
