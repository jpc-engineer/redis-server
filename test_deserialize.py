import pytest
from deserialize import Deserializer

simple_str = "+test\r\n"
error = "-ERR unknown command\r\n"
int_test = ":1000\r\n"
bulkstr_test = "$5\r\nhello\r\n"

@pytest.fixture
def deserializer():
    return Deserializer(bulkstr_test)

def test_decode_string(deserializer):
    #assert deserializer.decode_string() == "ERR unknown command"
    pass

def test_decode_integer(deserializer):
    #assert deserializer.decode_integer() == 1000
    pass

def test_decode_bulk_string(deserializer):
    assert deserializer.decode_bulk_string() == "hello"
    