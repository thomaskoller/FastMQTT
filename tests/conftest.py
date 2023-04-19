import pytest

from fastmqtt import FastMQTT


@pytest.fixture(scope="session")
def app() -> FastMQTT:
    return FastMQTT(host="localhost")
