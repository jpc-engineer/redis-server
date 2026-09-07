import pytest
from deserialize import Deserializer


error = "-ERR unknown command\r\n"
array_test = "*2\r\n$3\r\nfoo\r\n$3\r\nbar\r\n"

def test_decode_string():
    d = Deserializer("+test\r\n")
    result = d.decoder_dispatch()
    assert result == "test"

def test_decode_integer():
    d = Deserializer(":1000\r\n")
    result = d.decoder_dispatch()
    assert result == 1000 

def test_decode_bulk_string():
    d = Deserializer("$5\r\nhello\r\n")
    result = d.decoder_dispatch()
    assert result == "hello"

def test_decode_array():
    d = Deserializer("*2\r\n$3\r\nfoo\r\n$3\r\nbar\r\n")
    result = d.decoder_dispatch() 
    assert result == ["foo", "bar"]
