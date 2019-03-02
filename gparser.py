from Token import Token
from operations import Const, SimpleEdge, Operation, Name, Uniq, ParametrizedEdge, Len, Include, GenomeName, \
    Weights


class ParseException(Exception):
    pass


class GraphParser:
    __expression = ''
    __index = 0
    __size = 0
    __name = ''
    __value = ''
    __token = Token.FAIL
    __prev_token = None

    __last_params = None
    __FUNCTIONS = []  # array of function pointers. Order sets the priority of operations

    def __init__(self):
        super().__init__()
        self.__FUNCTIONS = [self.__edge, self.__primary]

    def next_token(self) -> Token:
        """ Function return next token in expression.
        :raise ParserException if token is not valid
        """
        self.__prev_token = self.__token
        tmp = self.__next_token_unchecked()
        if tmp == self.__prev_token:
            idx = self.__index

            self.__raise_wrong_token(idx - 1, "Unexpected token " + str(tmp.name))
        return tmp

    def __next_token_unchecked(self) -> Token:
        """ Function return next token in expression. """
        self.__skip_ws()

        if self.__size <= self.__index:
            return Token.END
        symbol = self.__expression[self.__index]
        self.__next_char()

        self.__token = Token.find(symbol)

        if self.__token != Token.FAIL:
            return self.__token

        start = self.__index - 1
        # Unused
        # if symbol.isalpha():
        #     while self.__is_correct_bound() and self.__current().isalpha():
        #         self.__next_char()
        #
        #     string = self.__expression[start: self.__index]
        #     token = Token.find(string)
        #     if token == Token.FAIL:
        #         self.__name = string
        #         return Token.NAME
        #     return token

        if symbol.isdigit():
            while self.__is_correct_bound() and self.__current().isdigit():
                self.__next_char()

            self.__value = int(self.__expression[start: self.__index])
            return Token.CONST
        return self.__token

    def __skip_ws(self):
        """ Function which skip all whitespaces from current expression index """
        while self.__is_correct_bound() and self.__expression[self.__index] == ' ':  # ws
            self.__index += 1

    def __is_correct_bound(self) -> bool:
        """ Function check if current index is in bound of expression """
        return self.__index < self.__size

    def __next_char(self):
        """ Increment current expression index """
        self.__index += 1

    def __current(self) -> str:
        """ Current expression char"""
        return self.__expression[self.__index]

    def __edge(self, new_token: bool):
        """ Function makes new edge"""
        left = self.__primary(new_token)

        while True:
            if self.__token == Token.OPEN_EDGE:
                self.__primary(False)  # parse params
            if self.__token == Token.EDGE:
                left = SimpleEdge(left, self.__next_priority(self.__edge, True))
            elif self.__token == Token.P_EDGE:
                left = ParametrizedEdge(left, self.__next_priority(self.__edge, True), self.__last_params)
                self.__last_params = list()
            else:
                return left

    def __primary(self, new_token: bool):
        """ Primary operations """

        if new_token:
            self.__token = self.next_token()

        if self.__token == Token.CONST:
            v = self.__value
            self.__token = self.next_token()
            return Const(v)

        if self.__token == Token.APOSTROPHE:
            """ if it's new vertex name"""
            self.__skip_ws()
            start = self.__index
            while self.__current() != Token.APOSTROPHE.value:
                self.__next_char()

            if not self.__is_correct_bound():
                raise ParseException("Wrong token at " + str(self.__index))

            new_name = self.__expression[start: self.__index]
            self.__next_char()
            self.__token = self.next_token()
            return Name(new_name)

        if self.__token == Token.OPEN_EDGE:
            start = self.__index
            while self.__is_correct_bound() and self.__current() != Token.CLOSE_EDGE.value:
                self.__next_char()

            if not self.__is_correct_bound():
                raise ParseException("Wrong token at " + str(self.__index))
            self.__last_params = self.__parse_edge_param(self.__expression[start: self.__index])
            self.__token = Token.P_EDGE
            self.__next_char()
            return

        # Unused
        # if self.__token == Token.UNIQ:
        #     print("hihihi")
        #     if self.__current() != Token.OPEN_BRACKET.value:
        #         self.__raise_wrong_token(self.__index)
        #
        #     self.__next_char()
        #     start = self.__index
        #     while self.__is_correct_bound() and self.__current() != ')':
        #         self.__next_char()
        #     args = [int(x) for x in self.__expression[start:self.__index].split(',')]
        #     self.__next_char()
        #     self.__token = self.next_token()
        #     return Uniq(args)

    def __next_priority(self, sender=None, new_token=False):
        """ helper function: call next priority from sender priority"""
        if sender is not None:
            for i in range(0, len(self.__FUNCTIONS)):
                if self.__FUNCTIONS[i] == sender:
                    return self.__FUNCTIONS[i + 1](new_token)
        return self.__FUNCTIONS[0](new_token)

    def __low_priority(self, new_token):
        """ Call lowest priority operation"""
        return self.__next_priority(new_token=new_token)

    def __parse_edge_param(self, params_string: str):
        return [self.__to_param(arg) for arg in params_string.split(Token.SEPARATOR_EDGE_PARAMS.value)]

    def parse(self, base: str):
        self.__expression = base
        self.__size = base.__len__()

        self.__token = self.next_token()

        while self.__index < self.__size and self.__token == Token.FAIL:
            self.__token = self.next_token()

        return Operation() if self.__token == Token.END else self.__next_priority(None, False)

    def __raise_wrong_token(self, index: int, message=''):
        message = 'Wrong token at ' + str(index) + '. ' + message + '\n' + self.__expression + '\n' + (
                ' ' * index + '^' + ' ' * (self.__size - index))
        raise ParseException(message)

    @staticmethod
    def __to_param(arg):
        arg = arg.replace(' ', '')
        if len(arg) == 0:
            return Len.default()
        token = Token.find(arg[0])
        idx = 0
        while idx < len(arg) and arg[idx] != Token.OPEN_BRACKET.value:
            idx += 1
        start = idx + 1
        while idx < len(arg) and arg[idx] != Token.CLOSE_BRACKET.value:
            idx += 1
        params_str = arg[start:idx]
        if token == Token.GENOME_NAME:
            return GenomeName([params_str])
        params = [int(x) for x in params_str.split(',')]
        if token == Token.UNIQ:
            return Uniq(params)
        if token == Token.LENGTH:
            return Len(params)
        if token == Token.LOCATION:
            return Include(params)
        if token == Token.WEIGHTS:
            return Weights(params)
