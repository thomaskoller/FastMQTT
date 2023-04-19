import typing

import paho.mqtt.client as mqtt

from .signature import CallbackSignature
from .topic import Topic


class FastMQTT:
    def __init__(self) -> None:
        self._broker = mqtt.Client()
        self._broker.connect(host="localhost", port=1883)
        self._broker.on_message = self._on_message
        self._topics: typing.Dict[Topic, CallbackSignature] = {}

    def subscribe(self, topic: str) -> typing.Callable:
        def inner(func: typing.Callable):
            self._topics[topic] = CallbackSignature.load(callback=func)
            self._broker.subscribe(topic=topic)

            def wrapped(msg):
                func(msg=msg)

            return wrapped

        return inner

    def run(self) -> typing.NoReturn:
        self._broker.loop_forever()

    def _on_message(self, client, user, msg) -> None:
        self._get_callback_signature(topic=msg.topic)(payload=msg.payload)

    def _get_callback_signature(self, topic: Topic) -> CallbackSignature:
        return self._topics[topic]
