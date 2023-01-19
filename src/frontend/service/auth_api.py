from functools import lru_cache
from typing import List

import aiohttp
from models.user import User, UserRole
from core.config import config


class AuthApiService:
    @staticmethod
    async def get_user_role(headers: dict) -> List[str]:
        """
        Запросить Роли Пользователя. Пользователь закодирован в заголовках, с помощью JWT-токена
        """
        async with aiohttp.ClientSession() as session:
            url = config.auth_api.address + "api/v1/me/roles"
            async with session.get(url, headers=headers) as resp:
                response = await resp.json()

        return [str(item) for item in response]

    @staticmethod
    async def get_user_info(headers: dict) -> User:
        """
        Получить информацию о Пользователе по JWT-токену в заголовке
        """
        async with aiohttp.ClientSession() as session:
            url = config.auth_api.address + "api/v1/me"
            async with session.get(url, headers=headers) as resp:
                response = await resp.json()

        return User(**response)


@lru_cache()
def get_auth_api_service() -> AuthApiService:
    return AuthApiService()
