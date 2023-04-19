import pydantic
import pytest


def test_can_subscribe_topic(app):
    topic = "test"

    @app.subscribe(topic=topic)
    def callback(msg: str):
        pass

    assert app._topics[topic]


@pytest.mark.skip
def test_can_subscribe_primitive(app):
    @app.subscribe(topic="primitive")
    def callback(msg: str) -> None:
        assert isinstance(msg, str)

    app.run()


@pytest.mark.skip
def test_can_subscribe_basemodel(app):
    class Model(pydantic.BaseModel):
        str: str
        int: int

    @app.subscribe(topic="dict")
    def callback(msg: Model) -> None:
        assert isinstance(msg, Model)

    app.run()
