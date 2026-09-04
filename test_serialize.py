import pytest
from serialize import Serializer

encode_test_str = "CONTENT"
encode_test_err = "ERR unknown command"
encode_test_int = "1000"
encode_test_bulk_str = "hello"
encode_test_array = ["set", "Name", "John"]

@pytest.fixture
def serializer():
    return Serializer(encode_test_array)

def test_encode_str(serializer):
    #assert serializer.encode_str() == "+CONTENT\r\n"
    pass

def test_encode_error(serializer):
    #assert serializer.encode_error() == "-ERR unknown command\r\n"
    pass

def test_encode_integer(serializer):
    #assert serializer.encode_integer() == ":1000\r\n"
    pass

def test_encode_bulk_string(serializer):
    #assert serializer.encode_bulk_string() == "$5\r\nhello\r\n"
    pass

def test_encode_array(serializer):
    #assert serializer.encode_array() == "*3\r\n$3\r\nset\r\n$4\r\nName\r\n$4\r\nJohn\r\n"
    pass
    