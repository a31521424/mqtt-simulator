import time
from typing import Optional

import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion

from config.config import Configured


class Topic:
    def __init__(self, config: Configured):
        self.config: Configured = config

        self.is_connected: bool = False

        self.connect = mqtt.Client(client_id=self.config.username, callback_api_version=CallbackAPIVersion.VERSION2)
        self.connect.username_pw_set(username=self.config.username, password=self.config.password)

        self.connect.on_connect = self.get_on_connect()
        self.connect.on_connect_fail = self.get_on_connect_fail()
        self.connect.on_message = self.get_on_messages()
        # self.connect.loop_start()  # 取消接受消息
        self.connect.connect(host=self.config.host, port=self.config.port, keepalive=self.config.keep_alive)

    def start(self):
        while True:
            self.send_message()
            time.sleep(self.config.cycle_time)

    def send_message(self):
        for topic in self.config.topics:
            upload_data = topic.generate_data()
            self.connect.publish(topic=topic.topic_url, payload=upload_data, )
            print(f'upload event {upload_data}')
            time.sleep(1)

    def get_on_connect(self):
        def func(client, userdata, flags, reason_code, properties):
            print(f"[connect]: {self.connect.username}")

        return func

    def get_on_connect_fail(self):
        def func():
            print(f"[connect fail]: {self.connect.username}")

        return func

    def get_on_messages(self):
        def func(client, userdata, msg: mqtt.MQTTMessage):
            print(f"[message]: {self.connect.username} {msg.payload}")

        return func
