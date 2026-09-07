class Deserializer:
    def __init__(self, value):
        self.value = value
        self.position = 1

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
        result = ""
        clean_value = self.value.replace("/r", "").replace("\n", "")
        for i in range(self.position, len(clean_value)):
            if clean_value[i] == '$':
                for item in clean_value:
                    content = Deserializer(item).decoder_dispatch()
                    result += content
        
        return result

    def decoder_dispatch(self):
        if self.value[0] == '+':
            self.position += 1
            return self.decode_string()
        elif self.value[0] == '-':
            self.position += 1
            return self.decode_string()    
        elif self.value[0] == ':':
            self.position += 1
            return self.decode_integer()    
        elif self.value[0] == '$':
            self.position += 1
            return self.decode_bulk_string()    
        elif self.value[0] == '*':
            self.position += 1
            return self.decode_array()

#d = Deserializer("*2\r\n$3\r\nfoo\r\n$3\r\nbar\r\n")
#d.decoder_dispatch()