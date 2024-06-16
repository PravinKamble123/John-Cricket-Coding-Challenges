# JsonParser

JsonParser is a command-line tool to validate JSON files without using the `json` library. This tool is designed to help you verify the correctness of JSON files and provide detailed error messages if the files are not valid.

## Features

- Validates JSON strings, arrays, objects, numbers, and literals (`true`, `false`, `null`).
- Provides detailed error messages for invalid JSON structures.
- Handles nested JSON structures and escaped characters in strings.

## Installation

1. Clone this repository to your local machine:

```bash
git clone https://github.com/PravinKamble123/John-Cricket-Coding-Challenges.git

cd jsonparser

# Usage
python jsonparser.py <filename>

# Example
python jsonparser.py example.json

```
## Error Messages
The tool provides detailed error messages to help you understand what went wrong with the JSON file. Common error messages include:

Invalid JSON value: Indicates that a value in the JSON file is not valid.
Invalid JSON string. Unescaped double quote found.: Indicates that a string contains an unescaped double quote.
Invalid JSON array: Indicates that the array structure is not valid.
Invalid JSON object: Indicates that the object structure is not valid.
Invalid number: Indicates that a number is not formatted correctly.
Numbers cannot have leading zeroes: Indicates that a number has leading zeroes, which is not allowed.
Numbers cannot be hex: Indicates that hexadecimal numbers are not allowed.
