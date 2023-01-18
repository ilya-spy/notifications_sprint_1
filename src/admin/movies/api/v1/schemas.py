import datetime
import uuid
from typing import List, Optional

from pydantic import BaseModel, Field


class Movie(BaseModel):
    id: uuid.UUID = Field(title="uuid")
    title: str = Field(title="Название")
    description: Optional[str] = Field(title="Описание")
    creation_date: Optional[datetime.datetime] = Field(title="Дата создания")
    rating: Optional[float] = Field(title="description: Рейтинг")
    type: Optional[str] = Field(title="Тип")
    genres: List[str] = Field(title="Список жанров", default_factory=list)
    actors: List[str] = Field(
        title="Список актёров", default_factory=list, alias="actor"
    )
    directors: List[str] = Field(
        title="Список режиссеров", default_factory=list, alias="director"
    )
    writers: List[str] = Field(
        title="Список сценаристов", default_factory=list, alias="writer"
    )


class MoviesList(BaseModel):
    count: int = Field(title="Количество объектов", ge=0)
    total_pages: int = Field(title="Количество страниц", ge=1)
    prev: Optional[int] = Field(title="Номер предыдущей страницы", ge=1)
    next: Optional[int] = Field(title="Номер следующей страницы", ge=2)
    results: List[Movie] = Field(title="Список сценаристов", default_factory=list)
