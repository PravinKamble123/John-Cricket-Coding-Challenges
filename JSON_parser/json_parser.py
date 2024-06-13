import argparse

class JsonParser:
    def __init__(self, filename):
        self.filename = filename
        self.text = self.read_file()
    
    def read_file(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Error: {self.filename} does not exist.")
            return ""
        except Exception as e:
            print(f"Error reading {self.filename}: {str(e)}")
            return ""

    def validate(self):
        if not self.text:
            return False
        return self.is_valid_json(self.text)

    def is_valid_json(self, text):
        try:
            self._parse_value(text.strip())
            return True
        except ValueError:
            return False

    def _parse_value(self, text):
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
            raise ValueError("Invalid JSON")

    def _parse_string(self, text):
        if text.endswith('"') and len(text) > 1:
            return text[1:-1]
        else:
            raise ValueError("Invalid JSON string")

    def _parse_array(self, text):
        if not text.endswith(']'):
            raise ValueError("Invalid JSON array")
        elements = text[1:-1].split(',')
        return [self._parse_value(el.strip()) for el in elements]

    def _parse_object(self, text):
        if not text.endswith('}'):
            raise ValueError("Invalid JSON object")
        items = text[1:-1].split(',')
        obj = {}
        for item in items:
            key, value = item.split(':')
            obj[self._parse_string(key.strip())] = self._parse_value(value.strip())
        return obj

    def _is_number(self, text):
        try:
            float(text)
            return True
        except ValueError:
            return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A CLI tool to validate JSON files without using the json library.")
    parser.add_argument('filename', type=str, help='The path to the JSON file to validate')
    args = parser.parse_args()

    json_parser = JsonParser(args.filename)
    if json_parser.validate():
        print(f"{args.filename} is valid JSON.")
    else:
        print(f"{args.filename} is not valid JSON.")
