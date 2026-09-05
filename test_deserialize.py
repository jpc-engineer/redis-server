import pytest
from deserialize import Deserializer

simple_str = "+test\r\n"
error = "-ERR unknown command\r\n"
int_test = ":1000\r\n"

@pytest.fixture
def deserializer():
    return Deserializer(int_test)

def test_decode_string(deserializer):
    #assert deserializer.decode_string() == "ERR unknown command"
    pass

def test_decode_integer(deserializer):
    assert deserializer.decode_integer() == 1000
    