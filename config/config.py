from __future__ import annotations

import json
import random
import time
from typing import Optional, List, Union

from pydantic import BaseModel


class Configured(BaseModel):
    host: Optional[str] = '127.0.0.1'
    port: Optional[int] = 1883
    username: str
    password: str
    keep_alive: Optional[int] = 30
    topics: List[TopicConfig] = []
    cycle_time: int = 30


class TopicConfig(BaseModel):
    channel: str
    sub_topic: Optional[str] = None
    unit: Optional[str] = None
    sensor_name: str = ""

    def generate_data(self) -> str:
        data = {
            "n": self.sensor_name,
            "v": self.computing_data(),
            "u": self.unit,
            "t": int(time.time())
        }
        return json.dumps(data)

    def computing_data(self) -> Union[str, int, float]:
        if self.unit == '°C':
            return random.uniform(0, 40)
        if self.unit == '%':
            return random.uniform(0, 100)
        if self.unit == "W":
            return random.uniform(0, 250)
        if self.unit == "A":
            return random.uniform(0, 20)
        if self.unit == "dB":
            return random.randrange(100)
        if self.unit == "AQI":
            return random.randrange(500)
        if self.unit == 'bool':
            return random.choice([True, False])
        return random.randint(0, 1000000)

    @property
    def topic_url(self):
        return f'channels/{self.channel}/messages' + (f'/{self.sub_topic}' if self.sub_topic else '')
