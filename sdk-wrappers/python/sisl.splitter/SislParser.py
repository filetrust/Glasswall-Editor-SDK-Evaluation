import binascii
import enum


class Sisl:
    name = None
    type = None
    value = None

    def __init__(self):
        pass


class SislParser:
    class SislTokenType(enum.Enum):
        ST_START = 0
        ST_GROUP_BEGIN = 1
        ST_GROUP_END = 2
        ST_WHITESPACE = 3
        ST_NAME = 4
        ST_TYPE = 5
        ST_VALUE_SEPARATOR = 6
        ST_VALUE = 7
        ST_DOUBLE_QUOTE = 8
        ST_PRINTABLE = 9
        ST_ESCAPE_LOWER_CASE_R = 10
        ST_ESCAPE_LOWER_CASE_T = 11
        ST_ESCAPE_LOWER_CASE_N = 12
        ST_ESCAPE_DOUBLE_QUOTE = 13
        ST_ESCAPE_BACK_SLASH = 14
        ST_ESCAPE_2HEX = 15
        ST_ESCAPE_4HEX = 16
        ST_ESCAPE_8HEX = 17
        ST_EOF = 18

    class SislToken:
        def __init__(self, type, size, offset):
            self.type = type
            self.size = size
            self.offset = offset

        def get_data(self, buffer):
            return buffer[self.offset: self.offset + self.size]

    @staticmethod
    def __is_alpha(character):
        return 'a' <= character <= 'z' or 'A' <= character <= 'Z'

    @staticmethod
    def __is_digit(character):
        return '0' <= character <= '9'

    @staticmethod
    def __is_whitespace(character):
        return character in [' ', '\r', '\n', '\t']

    @staticmethod
    def __is_hex(character):
        return SislParser.__is_digit(character) or 'a' <= character <= 'f' or 'A' <= character <= 'F'

    @staticmethod
    def __is_printable(character):
        return ' ' <= character <= '!' or '#' <= character <= '[' or ']' <= character <= '~'

    @staticmethod
    def __is_name_or_type_character(character):
        return SislParser.__is_alpha(character) or SislParser.__is_digit(
            character) or character == '.' or character == '_' or character == '-'

    @staticmethod
    def __is_name_or_type_valid(data):
        if len(data) < 1:
            return False

        current_character = data[0]

        if not (current_character == '_' or SislParser.__is_alpha(current_character)):
            return False

        for i in data[1:]:
            if not SislParser.__is_name_or_type_character(i):
                return False

        return True

    @staticmethod
    def __escape_value(data):

        result = bytearray()

        if len(data) == 0:
            return result

        for i in data:
            if SislParser.__is_printable(i):
                result += i
            else:
                result += b'\\'

                if i == b'"' or i == b'\\':
                    result += i
                elif i == '\r':
                    result += b'r'
                elif i == '\t':
                    result += b't'
                elif i == '\n':
                    result += b'n'
                else:
                    result += b'x' + binascii.hexlify(i)

        return result

    def __print_group_open(self, buffer):
        buffer += b'{'

        if SislParser.__pretty_print:
            buffer += b'\n'
            self.__indent_amount += 1

        self.__previous_token = SislParser.SislTokenType.ST_GROUP_BEGIN

    def __print_group_close(self, buffer):
        if self.__pretty_print:
            if self.__previous_token == SislParser.SislTokenType.ST_GROUP_END:
                buffer += b'\n'

            self.__indent_amount -= 1

            buffer += b' ' * (self.__indent_amount * 2)

        buffer += b'}'

        if self.__pretty_print:
            buffer += b'\n'

        self.__previous_token = SislParser.SislTokenType.ST_GROUP_END

    def __print_name(self, buffer, name):
        if self.__previous_token == SislParser.SislTokenType.ST_VALUE or self.__previous_token\
                == SislParser.SislTokenType.ST_GROUP_END:
            self.__print_value_separator(buffer)

        if self.__pretty_print:
            buffer += b' ' * (self.__indent_amount * 2)

        bytename = bytearray(name)

        if SislParser.__is_name_or_type_valid(bytename):
            buffer += bytename + b': '
        else:
            buffer += SislParser.SS_HEX_STR + binascii.hexlify(bytename) + b': '

        self.__previous_token = SislParser.SislTokenType.ST_NAME

    def __print_type(self, buffer, sisl_type):
        bytetype = bytearray(sisl_type)

        if self.__is_name_or_type_valid(bytetype):
            buffer += b'!' + bytetype + b' '
        else:
            buffer += b'!' + SislParser.SS_HEX_STR + binascii.hexlify(bytetype)

        self.__previous_token = SislParser.SislTokenType.ST_TYPE

    def __print_value(self, buffer, value):
        buffer += b'"'

        if len(value) > 0:
            buffer += SislParser.__escape_value(value)

        buffer += b'"'
        self.__previous_token = SislParser.SislTokenType.ST_VALUE

    def __print_value_separator(self, buffer):
        buffer += b','

        if self.__pretty_print:
            buffer += '\n'

        self.__previous_token = SislParser.SislTokenType.ST_VALUE_SEPARATOR

    def __get_name_or_type(self, buffer):
        pass

    def tokenize_sisl(self, buffer):
        self.__previous_token = SislParser.SislTokenType.ST_START
        current_offset = 0
        lexemes = []
        in_value_field = False
        lexemes.append(SislParser.SislToken(SislParser.SislTokenType.ST_START, 0, 0))

        while current_offset < len(buffer):
            previous_offset = current_offset
            current_character = buffer[current_offset]
            current_offset += 1

            if in_value_field:
                if current_character == '"':
                    in_value_field = False
                    self.__previous_token = SislParser.SislTokenType.ST_DOUBLE_QUOTE
                elif SislParser.__is_printable(current_character):
                    while current_offset < len(buffer) and SislParser.__is_printable(buffer[current_offset]):
                        current_offset += 1

                    self.__previous_token = SislParser.SislTokenType.ST_PRINTABLE
                elif current_character == '\\':
                    current_character = buffer[current_offset]
                    current_offset += 1

                    if current_character == 'r':
                        self.__previous_token = SislParser.SislTokenType.ST_ESCAPE_LOWER_CASE_R
                    elif current_character == 't':
                        self.__previous_token = SislParser.SislTokenType.ST_ESCAPE_LOWER_CASE_T
                    elif current_character == 'n':
                        self.__previous_token = SislParser.SislTokenType.ST_ESCAPE_LOWER_CASE_N
                    elif current_character == '"':
                        self.__previous_token = SislParser.SislTokenType.ST_ESCAPE_DOUBLE_QUOTE
                    elif current_character == '\\':
                        self.__previous_token = SislParser.SislTokenType.ST_ESCAPE_BACK_SLASH
                    elif current_character == 'x':
                        for i in buffer[current_offset: current_offset + 2]:
                            if not SislParser.__is_hex(i):
                                raise RuntimeError("Invalid escape character")

                        current_offset += 2

                        self.__previous_token = SislParser.SislTokenType.ST_ESCAPE_2HEX

                    elif current_character == 'u':
                        for i in buffer[current_offset: current_offset + 4]:
                            if not SislParser.__is_hex(i):
                                raise RuntimeError("Invalid escape character")

                        current_offset += 4

                        self.__previous_token = SislParser.SislTokenType.ST_ESCAPE_4HEX

                    elif current_character == 'U':
                        for i in buffer[current_offset: current_offset + 8]:
                            if not SislParser.__is_hex(i):
                                raise RuntimeError("Invalid escape character")

                        current_offset += 8

                        self.__previous_token = SislParser.SislTokenType.ST_ESCAPE_8HEX

                    else:
                        raise RuntimeError("Unknown escape found")
                else:
                    raise RuntimeError("Invalid character in value field")
            else:
                if SislParser.__is_whitespace(
                        current_character) and self.__previous_token != SislParser.SislTokenType.ST_START:
                    while current_offset < len(buffer) and SislParser.__is_whitespace(buffer[current_offset]):
                        current_offset += 1

                    self.__previous_token = SislParser.SislTokenType.ST_WHITESPACE

                elif current_character == '{':
                    self.__previous_token = SislParser.SislTokenType.ST_GROUP_BEGIN
                elif current_character == '}':
                    self.__previous_token = SislParser.SislTokenType.ST_GROUP_END
                elif current_character == '!':
                    while current_offset < len(buffer) and SislParser.__is_name_or_type_character(
                            buffer[current_offset]):
                        current_offset += 1

                    if (current_offset - previous_offset) <= 1:
                        raise RuntimeError("Type field is empty")

                    self.__previous_token = SislParser.SislTokenType.ST_TYPE
                elif current_character == ',':
                    self.__previous_token = SislParser.SislTokenType.ST_VALUE_SEPARATOR
                elif current_character == '"':
                    in_value_field = True
                    self.__previous_token = SislParser.SislTokenType.ST_DOUBLE_QUOTE
                else:
                    while current_offset < len(buffer) and SislParser.__is_name_or_type_character(
                            buffer[current_offset]):
                        current_offset += 1

                    current_character = buffer[current_offset]
                    current_offset += 1

                    if current_character != ':':
                        raise RuntimeError("Invalid name field")

                    self.__previous_token = SislParser.SislTokenType.ST_NAME

            size = current_offset - previous_offset

            lexemes.append(SislParser.SislToken(self.__previous_token, size, previous_offset))

        lexemes.append(SislParser.SislToken(self.__previous_token, 0, current_offset))

        return lexemes

    SS_NAME = b"__name"
    SS_NULL = b"__"
    SS_PATH = b"__path"
    SS_TYPE = b"__type"
    SS_PARTS = b"__parts"
    SS_FILE = b"__file"

    SS_HEX_STR = b"__hexstr_"

    __pretty_print = True

    def __init__(self):
        self.__previous_token = SislParser.SislTokenType.ST_START
        self.__indent_amount = 0

    def reset(self):
        self.__previous_token = SislParser.SislTokenType.ST_START
        self.__indent_amount = 0
