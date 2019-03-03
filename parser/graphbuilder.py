from parser.gparser import GraphParser
from parser.operations import Weights, Uniq, Contains, Len


# BioHack2019
# Belyaev Roman aka aprox13(git)

class Graph:
    """ Class for build graph to algorithm """

    def __init__(self):
        self.name_idx = 0
        self.name_var = 'X'
        self.normal = []
        self.not_normal = []

    def build(self, from_parser: list):

        res = [[], []]
        name_idx = 2
        weight_idx = 3
        len_idx = 4
        uniq_idx = 6
        contains_idx = 5

        names = set([x[name_idx] for x in from_parser])
        names.remove(None)
        for e in from_parser:

            if e[name_idx] is None:
                new_name = self.next_name()
                while new_name in names:
                    new_name = self.next_name()
                e[name_idx] = new_name

            default = [Weights.default().build(None), Len.default().build(None), Contains.default().build(None),
                       Uniq.default().build(None)]

            for i in [weight_idx, len_idx, contains_idx, uniq_idx]:
                if e[i] is None:
                    e[i] = default[i - weight_idx]
            simple_edge = (e[len_idx] == Len.default().build(None))

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
        for part in graph_str.split(';'):
            if part != '':
                GraphParser().parse(part).build(g)

        return Graph().build(g)

    @staticmethod
    def beautiful_parse(graph_str: str):
        """ beautiful output """
        res = Graph.parse(graph_str)

        def ft(x):
            return 'from ' + str(x[0]) + ' to ' + str(x[1])

        for row in res:
            for e in row:
                print("Edge {")
                print("\tFrom:    " + str(e[0]))
                print("\tTo:      " + str(e[1]))
                print("\tName:    " + str(e[2]))
                print("\tWeights: " + ft(e[3]))
                print("\tLength:  " + ft(e[4]))
                print("\tInclude: " + str(e[5]))
                print("\tUniq:    " + ft(e[6]))
                print('}')
