class Deserializer:
    def __init__(self, value):
        self.value = value
        self.position = 1

    def decode_string(self):
        str_result = []
        for i in range(self.position, len(self.value)):
            if self.value[i] != '\r' and self.value[i] != '\n':
                str_result.append(self.value[i])

        return "".join(str_result)

    def decode_integer(self):
        int_result = []
        for i in range(self.position, len(self.value)):
            if self.value[i] != '\r' and self.value[i] != '\n':
                int_result.append(self.value[i])

        ext_result = "".join(int_result)
        return int(ext_result)

    def decode_bulk_string(self):
        pass

    def decode_array(self):
        pass

    def decoder_dispatch(self):
        if self.value[0] == '+':
            return self.decode_string
        elif self.value[0] == '-':
            return self.decode_string()    
        elif self.value[0] == ':':
            return self.decode_integer()    
        elif self.value[0] == '$':
            return self.decode_bulk_string()    
        elif self.value[0] == '*':
            return self.decode_array()
