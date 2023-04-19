# FastMQTT

FastMQTT is a wrapper of the [paho-mqtt](https://github.com/eclipse/paho.mqtt.python) package which uses typing to parse the incoming message. Additionally one can use [pydantic](https://github.com/pydantic/pydantic) to get a validated model from an incoming json.

### Example
```
from fastmqtt import FastMQTT
import pydantic

class Payload(pydantic.BaseModel):
    param: str

app = FastMQTT()

@app.subscribe(topic="some/topic")
def some_topic(msg=Payload):
    """
    The some_topic function will be called 
    when a new message arrives at the topic 'some/topic'.
    The msg will be parsed automatically by it's defined type.
    """
    print(msg.param)
```