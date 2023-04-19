import pytest

from fastmqtt.signature import CallbackSignature


def test_can_load_callback_signature():
    def callback(param: str):
        return True

    callback_signature = CallbackSignature.load(callback=callback)
    assert callback_signature.callback == callback
    assert list(callback_signature.signature.parameters.keys()) == ["param"]
    assert callback_signature.signature.parameters["param"].annotation == str


@pytest.mark.parametrize(
    "payload, param_type, expectation",
    argvalues=[(b"String", str, "String"), (b"17", int, 17), (b"42.0", float, 42.0)],
    ids=["String", "Integer", "Float"],
)
def test_can_call_callback_signature(payload, param_type, expectation):
    class HasBeenCalled(Exception):
        pass

    def callback(msg: param_type):
        assert isinstance(msg, param_type)
        assert msg == expectation
        raise HasBeenCalled

    callback_signature = CallbackSignature.load(callback=callback)
    with pytest.raises(HasBeenCalled):
        callback_signature(payload=payload)
