import inspect
import json
import typing

import pydantic

Signature = inspect.Signature


class CallbackSignature(typing.NamedTuple):
    callback: typing.Callable
    signature: Signature

    def __call__(self, payload: bytes):
        decoded_payload = payload.decode("utf-8")
        signature_type = self._get_signature_type(key="msg")
        if issubclass(signature_type, pydantic.BaseModel):
            msg = signature_type(**json.loads(decoded_payload))
        else:
            msg = signature_type(decoded_payload)
        self.callback(msg=msg)

    @classmethod
    def load(cls, callback: typing.Callable) -> typing.Self:
        return cls(callback=callback, signature=inspect.signature(callback))

    def _get_signature_type(self, key: str) -> typing.Type:
        return self.signature.parameters[key].annotation
