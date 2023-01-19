from functools import lru_cache

from fastapi import Depends

from models.event import KafkaEvent
from db.kafka import get_kafka, AIOKafkaProducer

class EventStorageService:
    def __init__(self, kafka: AIOKafkaProducer):
        self.kafka = kafka

    async def send(self, topic_name: str, model: KafkaEvent) -> None:
        await self.kafka.send(topic=topic_name, key=model.key, value=model.value)

        return None


@lru_cache()
def get_event_storage_service(
    kafka: AIOKafkaProducer = Depends(get_kafka),
) -> EventStorageService:
    return EventStorageService(kafka)
