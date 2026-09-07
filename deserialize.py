class Deserializer:
    def __init__(self, value):
        self.value = value
        self.position = 0

    def decode_string(self):
        end = self.value.find('\r\n', self.position)

        if end == -1:
            end = len(self.value)

        current_line = self.value[self.position:end]

        self.position = end + 2

        return current_line

    def decode_integer(self):
        end = self.value.find('\r\n', self.position)

        if end == -1:
            end = len(self.value)

        current_value = self.value[self.position:end]

        self.position = end + 2

        return int(current_value)

    def decode_bulk_string(self):
        end = self.value.find('\r\n', self.position)

        if end == -1:
            end = len(self.value)

        strlen = self.value[self.position:end]

        self.position = end + 2

        strlen_int = int(strlen)
        if strlen_int == -1:
            return None
        
        current_str = self.value[self.position:self.position + strlen_int]

        self.position = self.position + strlen_int + 2
        
        return current_str

    def decode_array(self):
        end = self.value.find('\r\n', self.position)

        count = self.value[self.position:end]
        self.position = end + 2
        intcount = int(count)

        if intcount == -1:
            return None

        result = []

        for i in range(intcount):
            r = self.decoder_dispatch()
            result.append(r)
        
        return result

    def decoder_dispatch(self):
        char = self.value[self.position]
        self.position += 1
        if char == '+':
            return self.decode_string()
        elif char == '-':
            return self.decode_string()    
        elif char == ':':
            return self.decode_integer()    
        elif char == '$':
            return self.decode_bulk_string()    
        elif char == '*':
            return self.decode_array()
        else:
            raise ValueError(f"Unknown RESP type byte: {char}")