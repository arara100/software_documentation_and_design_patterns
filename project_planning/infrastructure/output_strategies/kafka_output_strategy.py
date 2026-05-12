import json
from typing import Any

from kafka import KafkaProducer

from business_logic.interfaces.i_output_strategy import IOutputStrategy


class KafkaOutputStrategy(IOutputStrategy):
    """Concrete strategy: serialises *data* as JSON and publishes to a Kafka topic."""

    def __init__(self, bootstrap_servers: str, topic: str) -> None:
        self._topic = topic
        self._producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v, default=str).encode("utf-8"),
        )

    def output(self, data: Any) -> None:
        self._producer.send(self._topic, value=data)
        self._producer.flush()
