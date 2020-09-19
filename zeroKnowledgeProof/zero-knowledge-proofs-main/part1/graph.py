import networkx as nx
import matplotlib.pyplot as plt

G=nx.Graph()
G.add_node("a")

exampleGraph = [
    (1, 2),
    (1, 4),
    (1, 3),
    (2, 5),
    (2, 5),
    (3, 6),
    (5, 6)
]
# G.add_nodes_from(["b","c"])
#
# G.add_edge(1,2)
# edge = ("d", "e")
# G.add_edge(*edge)
# edge = ("a", "b")
# G.add_edge(*edge)

# adding a list of edges:
# G.add_edges_from([("a","c"),("c","d"), ("a",1), (1,"d"), ("a",2)])
G.add_edges_from(exampleGraph)

print("Nodes of graph: ")
print(G.nodes())
print("Edges of graph: ")
print(G.edges())

nx.draw(G)
plt.savefig("simple_path.png") # save as png
plt.show() # display

# Python program to generate the all possible
# path of the graph from the nodes provided
# graph = {
#     'a': ['c'],
#     'b': ['d'],
#     'c': ['e'],
#     'd': ['a', 'd'],
#     'e': ['b', 'c']
# }
#
#
# # function to generate all possible paths
# def find_all_paths(graph, start, end, path=[]):
#     path = path + [start]
#     if start == end:
#         return [path]
#     paths = []
#     for node in graph[start]:
#         if node not in path:
#             newpaths = find_all_paths(graph, node, end, path)
#         for newpath in newpaths:
#             paths.append(newpath)
#     return paths
#
#
# # Driver function call to print all
# # generated paths
#
# # Python program to generate shortest path
#
# graph = {
#     'a': ['c'],
#     'b': ['d'],
#     'c': ['e'],
#     'd': ['a', 'd'],
#     'e': ['b', 'c']
# }
#
#
# # function to find the shortest path
# def find_shortest_path(graph, start, end, path=[]):
#     path = path + [start]
#     if start == end:
#         return path
#     shortest = None
#     for node in graph[start]:
#         if node not in path:
#             newpath = find_shortest_path(graph, node, end, path)
#             if newpath:
#                 if not shortest or len(newpath) < len(shortest):
#                     shortest = newpath
#     return shortest
#
#
# # Driver function call to print
# # the shortest path
# print(find_shortest_path(graph, 'd', 'c'))