import argparse

class JsonParser:
    def __init__(self, filename):
        self.filename = filename
        self.text = self.read_file()
        self.error_messages = []

    def read_file(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            self.error_messages.append(f"Error: {self.filename} does not exist.")
            return ""
        except Exception as e:
            self.error_messages.append(f"Error reading {self.filename}: {str(e)}")
            return ""

    def validate(self):
        if not self.text:
            return False
        return self.is_valid_json(self.text)

    def is_valid_json(self, text):
        try:
            self._parse_value(text.strip())
            return True
        except ValueError as e:
            self.error_messages.append(str(e))
            return False

    def _parse_value(self, text):
        text = text.strip()
        if text.startswith('"'):
            return self._parse_string(text)
        elif text.startswith('['):
            return self._parse_array(text)
        elif text.startswith('{'):
            return self._parse_object(text)
        elif text in ("true", "false", "null"):
            return text
        elif self._is_number(text):
            return text
        else:
            raise ValueError(f"Invalid JSON value: {text}")

    def _parse_string(self, text):
        
        if len(text) >= 2 and text[0] == '"' and text[-1] == '"':
            escaped = False
            
            arr = text[1:-1].split(':')
            
            if len(arr) == 2:
                return self._parse_string(arr[1])
            for i in range(1, len(text) - 1):
                if text[i] == '"' and not escaped:
                    raise ValueError(f"{text}: Invalid JSON string. Unescaped double quote found.")
                if text[i] == '\\' and not escaped:
                    escaped = True
                else:
                    escaped = False
            return text[1:-1]
        
        else:
            if text.startswith("\\"):
                
                self.error_messages.append(f"Illegal backslash escape: {text}")
                return False
            else:
                raise ValueError(f"{text}: Invalid JSON string. Missing closing '\"' or string too short.")

    def _parse_array(self, text):
        if not text.endswith(']'):
            raise ValueError("Invalid JSON array")
        if text[1:-1] == '':
            return True
        elements = self._split_elements(text[1:-1], ',')
        return [self._parse_value(el.strip()) for el in elements]

    def _parse_object(self, text):
        if not text.endswith('}'):
            raise ValueError("Invalid JSON object")
        if len(text) == 2:
            return {}
        items = self._split_elements(text[1:-1], ',')
        obj = {}
        for item in items:
            key, value = self._split_key_value(item)
            obj[self._parse_string(key.strip())] = self._parse_value(value.strip())
        return obj

    def _split_key_value(self, item):
        colon_index = item.find(':')
        if colon_index == -1:
            raise ValueError(f"Invalid JSON object: Missing colon in {item}")
        return item[:colon_index], item[colon_index + 1:]

    def _is_number(self, text):
        try:
            if text.isdigit():
                if text[0] == "0":
                    self.error_messages.append(f"Numbers cannot have leading zeroes: {text}")
                    return False
            elif text[:2] == "0x":
                self.error_messages.append(f"Numbers cannot be hex: {text}")
                return False
            float(text)
            return True
        except ValueError:
            raise ValueError(f"Invalid number: {text}")

    def _split_elements(self, text, delimiter):
        elements = []
        start = 0
        brackets = 0
        in_string = False
        for i, char in enumerate(text):
            if char == '"':
                in_string = not in_string
            elif not in_string:
                if char in '{[':
                    brackets += 1
                elif char in '}]':
                    brackets -= 1
                elif char == delimiter and brackets == 0:
                    elements.append(text[start:i])
                    start = i + 1
        elements.append(text[start:])
        return elements


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A CLI tool to validate JSON files without using the json library.")
    parser.add_argument('filename', type=str, help='The path to the JSON file to validate')
    args = parser.parse_args()

    json_parser = JsonParser(args.filename)
    if json_parser.validate():
        print(f"{args.filename} is valid JSON.")
        exit(0)
    else:
        print(f"{args.filename} is not valid JSON.")
        for error in json_parser.error_messages:
            print(error)
        exit(1)
