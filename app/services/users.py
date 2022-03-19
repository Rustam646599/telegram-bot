import os

from loguru import logger
from requests import exceptions
import requests

BASE_URL = os.getenv('SERVER_URL')


class User:
    """Модель юзера"""

    def __init__(self, user_id):
        self.user_id = user_id
        self.user = self.get_user()

    def is_register(self) -> bool:
        """Возвращает зарегистрирован ли юзер"""

        return bool(self.user)

    def register_user(self, name: str, phone: str) -> bool:
        data = {
            'uid': self.user_id,
            'name': name,
            'phone': phone
        }
        try:
            response = requests.post(f'{BASE_URL}users/', json=data)
            if response.status_code == requests.codes.created:
                self.user = response.json()
        except Exception as e:
            logger.info(str(e))
        finally:
            return self.is_register()

    def get_user(self) -> dict:
        """Возвращает объект юзера из backend или пустой словарь."""

        try:
            response = requests.get(f'{BASE_URL}users/{self.user_id}/')
            if response.status_code == requests.codes.ok:
                return response.json()
            return dict()
        except Exception as e:
            logger.info(str(e))
            return dict()

    def get_name(self) -> str:
        """Возвращает имя юзера"""

        return self.user.get('name', '')

    def save_video(self, data) -> bool:
        """Загружает видео в бэкенд и получает ответ об успешности."""

        try:
            data.update({'tg_user': self.user['id']})
            response = requests.post(f'{BASE_URL}posts/', json=data)
            if response.status_code == requests.codes.created:
                return True
            return False
        except Exception as e:
            logger.info(str(e))
            return False
