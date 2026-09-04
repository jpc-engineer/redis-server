import sys

class Serializer:
    def __init__(self, value):
        self.value = value
        self.terminator = "\r\n"

    def encode_str(self):
        if "\n" in self.value or "\r" in self.value:
            raise ValueError("Simple strings cannot contain terminator characters")

        return f"+{self.value}{self.terminator}"
    
    def encode_error(self):
        return f"-{self.value}{self.terminator}"
    
    def encode_integer(self):
        int_value = int(self.value)
        return f":{int_value}{self.terminator}"
    
    def encode_bulk_string(self):
        if self.value is None:
            return f"$-1{self.terminator}"
        
        if self.value == "":
            return f"$0{self.terminator}{self.terminator}"
        
        byte_size = len(self.value.encode('utf-8'))
        return f"${byte_size}{self.terminator}{self.value}{self.terminator}"
    
    def encode_array(self):
        if self.value is None:
            return f"*-1{self.terminator}"
        
        if len(self.value) == 0:
            return f"*0{self.terminator}"
        
        result = f"*{len(self.value)}{self.terminator}"

        for item in self.value:
            content = Serializer(item).encoder_dispatch()
            result += content

        return result
        
    def encoder_dispatch(self):
        if isinstance(self.value, list):
            return self.encode_array()
        elif isinstance(self.value, int):
            return self.encode_integer()
        elif isinstance(self.value, str):
            return self.encode_bulk_string()
        elif self.value is None:
            return self.encode_bulk_string()
        else:
            raise ValueError("Unsupported type")
        


    