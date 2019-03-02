from enum import Enum


class Token(Enum):
    FAIL = 0
    START = 1
    END = 2
    NAME = 3
    CONST = 4
    OPEN_EDGE = '{'
    CLOSE_EDGE = '}'
    EDGE = '>'
    OPEN_BRACKET = '('
    CLOSE_BRACKET = ')'
    APOSTROPHE = '\''
    SEPARATOR_EDGE_PARAMS = ':'
    LENGTH = 'l'
    LOCATION = 'n'
    WEIGHTS = 'w'
    GENOM_NAME = 'g'
    UNIQ = 'u'
    P_EDGE = 5

    @staticmethod
    def find(symbol: str):
        for name, member in Token.__members__.items():
            if member.value == symbol:
                return member
        return Token.FAIL

    @classmethod
    def val(cls):
        return cls.value
