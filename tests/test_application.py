import json

import pydantic
import pytest


def test_can_subscribe_topic(app):
    topic = "test"

    @app.subscribe(topic=topic)
    def callback(msg: str):
        pass

    assert app._topics[topic]


@pytest.mark.skip(reason="Local development")
@pytest.mark.parametrize(
    "topic, payload",
    argvalues=[
        ("topic", "test"),
        ("topic", b"bytes"),
        ("topic", 17),
        ("topic", 42.0),
        ("topic", json.dumps({"key": "test"})),
    ],
    ids=["String", "Bytes", "Integer", "Float", "Json"],
)
def test_can_publish_to_topic(app, topic, payload):
    app.publish(topic=topic, payload=payload)


@pytest.mark.skip(reason="Local development")
def test_can_subscribe_primitive(app):
    @app.subscribe(topic="primitive")
    def callback(msg: str) -> None:
        assert isinstance(msg, str)

    app.run()


@pytest.mark.skip(reason="Local development")
def test_can_subscribe_basemodel(app):
    class Model(pydantic.BaseModel):
        str: str
        int: int

    @app.subscribe(topic="dict")
    def callback(msg: Model) -> None:
        assert isinstance(msg, Model)

    app.run()
