import random
import inspect
import networkx as nx
import matplotlib.pyplot as plt
# import numpy as np
import igraph
from igraph import *
import networkx.algorithms.isomorphism as iso
# import matplotlib.pyplot, pylab
# import sys
# import gra

# a graph is a list of edges, and for simplicity we'll say
# every vertex shows up in some edge
exampleGraph = [
    (1, 2),
    (1, 4),
    (1, 3),
    (2, 5),
    (2, 5),
    (3, 6),
    (5, 6)
]


def numVertices(G):
    return max(v for e in G for v in e)


def randomPermutation(n):
    L = list(range(n))
    # print("List of range n=6 is ", L)
    random.shuffle(L)
    L = [3, 4, 2, 0, 1, 5]
    # print("shuffled L list is = ", L)
    return L


def makePermutationFunction(L):
    # L = [3, 4, 2, 0, 1, 5]
    # m = lambda i: L[i - 1] + 1
    # print("lambda = ", m(2))
    return lambda i: L[i - 1] + 1


def makeInversePermutationFunction(L):
    return lambda i: 1 + L.index(i - 1)


def applyIsomorphism(G, f):
    # L = [3, 4, 2, 0, 1, 5]
    # f = lambda i: L[i - 1] + 1
    # finv = f = lambda i: 1 + L.index(i - 1)
    # G1 = [(1, 2), (1, 4), (1, 3), (2, 5), (2, 5), (3, 6), (5, 6)]
    # G2 = [(4, 5), (4, 1), (4, 3), (5, 2), (5, 2), (3, 6), (2, 6)]
    # G = [(4, 5), (4, 1), (4, 3), (5, 2), (5, 2), (3, 6), (2, 6)]
    # G = [(1, 2), (1, 4), (1, 3), (2, 5), (2, 5), (3, 6), (5, 6)]

    # print("G is = ", G)
    # for (i, j) in G:
    # f = lambda i: L[i - 1] + 1
    # f = lambda i: 1 + L.index(i - 1)
    #     print("i is =", i)
    #     print("f(", i, ") is ", f(i))
    return [(f(i), f(j)) for (i, j) in G]


def generate_edges(graph):
    edges = []
    for node, node1 in graph:
        edges.append((node, node1))
        # for neighbour in graph[node]:
        #     edges.append((node, neighbour))

    print("generated edges = ", edges)
    return edges


def drawIsomorphic(n, G1):
    # for _ in 2:
    g1 = nx.Graph()
    # g1.add_node("a")
    g1.add_edges_from(G1)
    nx.draw(g1)
    plt.savefig("G1.png")  # save as png
    plt.show()  # display
    # return g1


def isIsomorphism(n, G1, G2):
    drawIsomorphic(n, G1)

    # g1 = nx.DiGraph()
    # g2 = nx.DiGraph()
    # nx.add_path(G1, G1, weight=1)
    # nx.add_path(G2, G2, weight=2)
    # em = iso.numerical_edge_match("weight", 1)
    # nx.is_isomorphic(G1, G2)  # no weights considered
    # g = nx.is_isomorphic(G1, G2)
    # print("is isomorphic? ", g)

    g1 = nx.MultiDiGraph()
    g2 = nx.MultiDiGraph()
    g1.add_nodes_from(G1, fill="red")
    g2.add_nodes_from(G2, fill="red")
    nx.add_path(g1, G1, weight=3, linewidth=2.5)
    nx.add_path(g2, G2, weight=3)
    nm = iso.categorical_node_match("fill", "red")
    nx.is_isomorphic(g1, g2, node_match=nm)
    g = nx.is_isomorphic(g1, g2, node_match=nm)
    print("is isomorphic? ", g)

    g3 = nx.Graph()
    # g1.add_node("a")
    g3.add_edges_from(G2)
    nx.draw(g3)
    plt.savefig("G2.png")  # save as png
    plt.show()

    return g


class Prover(object):
    def __init__(self, G1, G2, isomorphism):
        '''
            isomomorphism is a list of integers representing
            an isomoprhism from G1 to G2.
        '''
        # G1 is = [(1, 2), (1, 4), (1, 3), (2, 5), (2, 5), (3, 6), (5, 6)]
        # G2 is = [(4, 5), (4, 1), (4, 3), (5, 2), (5, 2), (3, 6), (2, 6)]
        # isomorphism = p = [3, 4, 2, 0, 1, 5]
        self.G1 = G1
        self.G2 = G2
        self.n = numVertices(G1)
        # print("no. of vertices in G1 = ", numVertices(G1)) = 6
        assert self.n == numVertices(G2)
        # print("no. of vertices in G2 = ", numVertices(G2)) = 6

        self.isomorphism = isomorphism
        self.state = None

    def sendIsomorphicCopy(self):
        # self.n = 6
        isomorphism = randomPermutation(self.n)
        # print(" randomPermutation of 6 = ", isomorphism) = [3, 4, 2, 0, 1, 5]
        pi = makePermutationFunction(isomorphism)
        # print("makePermutationFunction of isomorphism = ", pi) = lambda i: L[i - 1] + 1
        H = applyIsomorphism(self.G1, pi)
        # print(" H is ", H)  = H is  [(4, 5), (4, 1), (4, 3), (5, 2), (5, 2), (3, 6), (2, 6)] = G2
        self.state = isomorphism  # = [3, 4, 2, 0, 1, 5]
        return H

    def proveIsomorphicTo(self, graphChoice):
        # graphChoice = (1 / 2)
        # graphChoice = 1
        randomIsomorphism = self.state
        # print("Prover self.state = ", randomIsomorphism) = [3, 4, 2, 0, 1, 5]
        piInverse = makeInversePermutationFunction(randomIsomorphism)
        # piInverse = lambda i: 1 + L.index(i - 1) given L = randomIsomorphism) = [3, 4, 2, 0, 1, 5]

        # print("Prover graphChoice = ", graphChoice)
        if graphChoice == 1:
            # print("Prover pragpChoice is ", graphChoice, " thus return piInverse = ")
            return piInverse
        else:
            f = makePermutationFunction(self.isomorphism)
            # f = lambda i: L[i - 1] + 1 given L = isomorphism) = [3, 4, 2, 0, 1, 5]
            # print("Prover pragpChoice is", graphChoice, " thus return = f")
            return lambda i: f(piInverse(i))


class Verifier(object):
    def __init__(self, G1, G2):
        # G1 is = [(1, 2), (1, 4), (1, 3), (2, 5), (2, 5), (3, 6), (5, 6)]
        # G2 is = [(4, 5), (4, 1), (4, 3), (5, 2), (5, 2), (3, 6), (2, 6)]
        self.G1 = G1
        self.G2 = G2
        self.n = numVertices(G1)
        # print("no. of vertices in G1 = ", numVertices(G1)) = 6
        assert self.n == numVertices(G2)
        # print("no. of vertices in G2 = ", numVertices(G2)) = 6

    def chooseGraph(self, H):
        # H = G2 = [(4, 5), (4, 1), (4, 3), (5, 2), (5, 2), (3, 6), (2, 6)] == G2
        choice = random.choice([1, 2])  # Randomly choose values between 1 and 2 i.e 1 or 2
        # print("Verrifier choice = ", choice) = 1 or 2 randomly chosen
        self.state = H, choice
        # print("Verifier self.state = ", self.state) = ([(4, 5), (4, 1), (4, 3), (5, 2), (5, 2), (3, 6), (2, 6)], 2 / 1)
        return choice

    def accepts(self, isomorphism):
        # isomorphism = piInverse = lambda i: 1 + L.index(i - 1) given L = randomIsomorphism) = [3, 4, 2, 0, 1, 5]  OR f = lambda i: L[i - 1] + 1 given L = isomorphism) = [3, 4, 2, 0, 1, 5]
        '''
            Return True if and only if the given isomorphism
            is a valid isomorphism between the randomly
            chosen graph in the first step, and the H presented
            by the Prover.
        '''
        # H = G2 = [(4, 5), (4, 1), (4, 3), (5, 2), (5, 2), (3, 6), (2, 6)] == G2
        # choice = 1 / 2
        # G1 is = [(1, 2), (1, 4), (1, 3), (2, 5), (2, 5), (3, 6), (5, 6)]
        # G2 is = [(4, 5), (4, 1), (4, 3), (5, 2), (5, 2), (3, 6), (2, 6)]
        # choice = 2
        H, choice = self.state
        graphToCheck = [self.G1, self.G2][choice - 1]
        # print("concatenate = ", [self.G1, self.G2]) =  [[(1, 2), (1, 4), (1, 3), (2, 5), (2, 5), (3, 6), (5, 6)], [(4, 5), (4, 1), (4, 3), (5, 2), (5, 2), (3, 6), (2, 6)]]
        # print("choice - 1 = ", [choice - 1]).... If choice is 1, [choice - 1] = [0] , if choice is 2, [choice - 1] is [1]
        # print("Verifier grapgh to check is  = ", graphToCheck).... If choice is 1, graphToCheck = G1 , if choice is 2, graphToCheck is G2
        f = isomorphism
        # f =  isomorphism = piInverse = lambda i: 1 + L.index(i - 1) given L = randomIsomorphism) = [3, 4, 2, 0, 1, 5]  OR f = lambda i: L[i - 1] + 1 given L = isomorphism) = [3, 4, 2, 0, 1, 5]

        # print("Verifier final  H = ", H)
        # print("Verifier final  f = ", f)
        isValidIsomorphism = (graphToCheck == applyIsomorphism(H, f))  # = applyIsomorphism(G2, f)
        # print("Verifier graphToCheck = ", graphToCheck)
        # print("Verifier applyIsomorphism = ", applyIsomorphism(H, f))
        # print("Verifier isValidIsomorphism = ", isValidIsomorphism)
        return isValidIsomorphism


def runProtocol(G1, G2, isomorphism):
    # G1 is = [(1, 2), (1, 4), (1, 3), (2, 5), (2, 5), (3, 6), (5, 6)]
    # G2 is = [(4, 5), (4, 1), (4, 3), (5, 2), (5, 2), (3, 6), (2, 6)]
    # isomorphism = p = [3, 4, 2, 0, 1, 5]
    p = Prover(G1, G2, isomorphism)
    # print("runProtocol p = ", p)
    v = Verifier(G1, G2)
    # print("runProtocol v = ", v)

    H = p.sendIsomorphicCopy()
    # print("runProtocol H = ", H) = [(4, 5), (4, 1), (4, 3), (5, 2), (5, 2), (3, 6), (2, 6)] == G2
    choice = v.chooseGraph(H)
    # choice =  2 / 1

    witnessIsomorphism = p.proveIsomorphicTo(choice)
    # witnessIsomorphism = print("Prover pragpChoice is 1 thus return piInverse = ") OR ("Prover pragpChoice is 2)
    # thus return f = ")

    return v.accepts(witnessIsomorphism)  # returns True if G2 ==G2 when choice is 2 OR True if G1 ==G1 when choice is 1


def convinceBeyondDoubt(G1, G2, isomorphism, errorTolerance=1e-20):
    # G1 is = [(1, 2), (1, 4), (1, 3), (2, 5), (2, 5), (3, 6), (5, 6)]
    # G2 is = [(4, 5), (4, 1), (4, 3), (5, 2), (5, 2), (3, 6), (2, 6)]
    # isomorphism = p = [3, 4, 2, 0, 1, 5]
    probabilityFooled = 1

    # print("IS probabilityFooled > errorTolerance", probabilityFooled > errorTolerance)
    while probabilityFooled > errorTolerance:
        result = runProtocol(G1, G2, isomorphism)
        # print("RESULT = ", result) = True
        assert result
        # print("assert result") if result = False it gives AssertionError
        probabilityFooled *= 0.5
        # print("probabilityFooled is = ", probabilityFooled)
        # print(probabilityFooled)


#     Loop continnues 68 times until probabilityFooled <(less than) errorTolerance each time running the runProtocol function and giving result = True


def messagesFromProtocol(G1, G2, isomorphism):
    # G1 is = [(1, 2), (1, 4), (1, 3), (2, 5), (2, 5), (3, 6), (5, 6)]
    # G2 is = [(4, 5), (4, 1), (4, 3), (5, 2), (5, 2), (3, 6), (2, 6)]
    p = Prover(G1, G2, isomorphism)
    v = Verifier(G1, G2)

    H = p.sendIsomorphicCopy()
    choice = v.chooseGraph(H)
    witnessIsomorphism = p.proveIsomorphicTo(choice)

    return [H, choice, witnessIsomorphism]


def simulateProtocol(G1, G2):
    # Construct data drawn from the same distribution as what is
    # returned by messagesFromProtocol
    # G1 is = [(1, 2), (1, 4), (1, 3), (2, 5), (2, 5), (3, 6), (5, 6)]
    # G2 is = [(4, 5), (4, 1), (4, 3), (5, 2), (5, 2), (3, 6), (2, 6)]
    choice = random.choice([1, 2])
    G = [G1, G2][choice - 1]
    n = numVertices(G)

    isomorphism = randomPermutation(n)
    pi = makePermutationFunction(isomorphism)
    H = applyIsomorphism(G, pi)

    return H, choice, pi


if __name__ == "__main__":
    G1 = exampleGraph

    # data = [(62725984, 63548262), (64797631, 64619047), (65069350, 65398449), (58960696, 57416785),
    #         (58760119, 58666604), (60470606, 61338129), (60728760, 59001882)]
    # data = G1
    # matplotlib.pyplot.scatter(*zip(*data))
    # matplotlib.pyplot.show()
    # A = np.array(G1)
    #
    # Flattened_X = A.flatten()
    # print(Flattened_X)
    #
    # print(A.flatten(order="C"))
    # print(A.flatten(order="F"))
    # print(A.flatten(order="A"))
    print("G1 is =", G1)
    n = numVertices(G1)
    print("number of vertices n =", n)
    # drawIsomorphic(n, G1)

    p = randomPermutation(n)
    print("random permutation p= ", p)
    f = makePermutationFunction(p)
    print("make permutation Function f = ", inspect.getsource(makePermutationFunction(p)))
    finv = makeInversePermutationFunction(p)
    print("make Inverse Permutation Function finv = ", finv)

    G2 = applyIsomorphism(G1, f)
    print("G2 = ", G2)
    print("finally G1 = ", G1)
    assert applyIsomorphism(G1, f) == G2
    assert applyIsomorphism(G2, finv) == G1

    convinceBeyondDoubt(G1, G2,
                        p)  # Runs a number of time to verify if true is really true in all the given loops e.g 68 times

    isIsomorphism(n, G1, G2)
    # graph = isIsomorphism(n, G1, G2)

    # g1 = nx.Graph()
    # g1.add_node("a")
    # nx.draw(graph)
    # plt.savefig("finalGraph.png")  # save as png
    # plt.show()  # display

    g2 = nx.Graph()
    # g2.add_node("a")
    # nx.draw(G1)
    # plt.savefig("G1.png")  # save as png
    # plt.show()  # display
    #
    # g3 = nx.Graph()
    # g3.add_node("a")
    # nx.draw(G2)
    # plt.savefig("G2.png")  # save as png
    # plt.show()  # display
