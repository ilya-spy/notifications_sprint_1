import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    """Десериализатор объекта в json строку"""
    return orjson.dumps(v, default=default).decode()


class BaseModel(BaseModel):
    """Базовый класс для всех Моделей данных.
    Переопределён сериализатор/десериализатор
    """

    class Config:
        """Конфиг"""

        json_loads = orjson.loads
        json_dumps = orjson_dumps
