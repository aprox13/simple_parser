from enum import Enum

# BioHack2019
# Belyaev Roman aka aprox13

class Token(Enum):
    FAIL = 0
    START = 1
    END = 2
    CONST = 4
    P_EDGE = 5
    OPEN_EDGE = '{'
    CLOSE_EDGE = '}'
    EDGE = '>'
    OPEN_BRACKET = '('
    CLOSE_BRACKET = ')'
    APOSTROPHE = '\''

    # PARAMS
    SEPARATOR_EDGE_PARAMS = ':'
    LENGTH = 'l'
    LOCATION = 'n'
    WEIGHTS = 'w'
    GENOME_NAME = 'g'
    UNIQ = 'u'

    @staticmethod
    def find(symbol: str):
        for name, member in Token.__members__.items():
            if member.value == symbol:
                return member
        return Token.FAIL

    @classmethod
    def val(cls):
        return cls.value
