from gparser import GraphParser
from operations import Weights, Uniq, Location, Len


class Graph:

    def __init__(self):
        self.name_idx = 0
        self.name_var = 'X'
        self.normal = []
        self.not_normal = []

    def build(self, from_parser: list):
        # print(str(from_parser))

        res = [[], []]
        NAME = 2
        WEIGHT = 3
        LEN = 4
        UNIQ = 5
        N = 6

        # edge ( from, to, name, weights,len, uniq, n)

        names = set([x[NAME] for x in from_parser])
        names.remove(None)
        for e in from_parser:
            if e[NAME] is None:
                new_name = self.next_name()
                while new_name in names:
                    new_name = self.next_name()
                e[NAME] = new_name

            default = [Weights.default().build(None), Len.default().build(None), Location.default().build(None),
                       Uniq.default().build(None)]

            for i in [WEIGHT, LEN, UNIQ, N]:
                if e[i] is None:
                    e[i] = default[i - WEIGHT]
            simple_edge = (e[LEN] == Len.default().build(None))

            if simple_edge:
                res[0].append(e)
            else:
                res[1].append(e)

        return res

    def next_name(self):
        self.name_idx += 1
        return self.name_var + '_' + str(self.name_idx - 1)

    @staticmethod
    def parse(graph_str: str):
        g = []
        input = graph_str.split(';')
        for part in input:
            if part != '':
                GraphParser().parse(part).build(g)

        return Graph().build(g)
