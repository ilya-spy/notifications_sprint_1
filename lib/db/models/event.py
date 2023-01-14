
import uuid

from pydantic import BaseModel


class Evennt(BaseModel):
    '''Используем одну универсальную таблицу для записи юзер-событий о фильмах, рецензиях, лайках'''
    '''Содержит универсальный набор полей для генерации событий из Джанго'''

    # primary key
    id: str

    # identifier for an initiator
    user_id: str
    username: str
    
    # film to which event is related
    film_id: str
    film_name: str

    # like, comment, bookmark
    event_type: str

    # for storing review text, if attached to event
    event_body: str
