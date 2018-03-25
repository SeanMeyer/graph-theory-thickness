''' Quick Refrence for Graph-Tool
#empty graph
g = Graph()
#undirected graph
ug = Graph(directed=False)
assert ug.is_directed()

v1 = g.add_vertex()
v2 = g.add_vertex()
e = g.add_edge(v1, v2)
graph_draw(
    g,
    vertex_text=g.vertex_index, 
    vertex_font_size=18,
    output_size=(200, 200), 
    output="two-nodes.png")

#Since graphs are uniquely identifiable by their indexes, you can just keep track of that
# g.add_edge(g.vertex(0), g.vertex(1)), would have worked
'''

#Import graph tool into the main namespace
from graph_tool.all import *
import re

#some graphs from competitionGraphs2018.nb
edgesOfGraph2 = '{{1, 5}, {1, 8}, {1, 14}, {1, 16}, {1, 17}, {1, 18}, {1, 20}, {1, 23}, {2, 6}, {2, 7}, {2, 13}, {2, 21}, {2, 22}, {2, 26}, {2, 31}, {2, 32}, {2, 33}, {3, 4}, {3, 6}, {3, 9}, {3, 15}, {3, 16}, {3,18}, {3, 25}, {3, 27}, {3, 30}, {4, 6}, {4, 9}, {4, 15}, {4, 18}, {4, 20}, {4, 25}, {4, 27}, {4, 30}, {5, 8}, {5, 14}, {5, 16}, {5, 17}, {5, 18}, {5, 20}, {5, 23}, {6, 7}, {6, 9}, {6, 13}, {6, 15}, {6, 21}, {6, 27}, {6, 30}, {6, 31}, {6, 32}, {6, 33}, {7, 13}, {7, 21}, {7, 22}, {7, 24}, {7, 29}, {7, 32}, {7, 33}, {8, 14}, {8, 16}, {8, 17}, {8, 18}, {8, 20}, {8, 23}, {9, 15}, {9, 16}, {9, 18}, {9, 25}, {9, 27}, {9, 30}, {10, 11}, {10, 12}, {10, 19}, {10, 21}, {10, 24}, {10, 26}, {10, 28}, {10, 29}, {10, 31}, {11, 12}, {11, 19}, {11, 21}, {11, 24}, {11, 26}, {11, 28}, {11, 29}, {11, 31}, {12, 19}, {12, 24}, {12, 26}, {12, 28}, {12, 29}, {12, 31}, {12, 32}, {13, 21}, {13, 22}, {13, 24}, {13, 31}, {13, 32}, {13, 33}, {14, 15}, {14, 16}, {14, 17}, {14, 20}, {14, 22}, {14, 23}, {14, 24}, {15, 16}, {15, 25}, {15, 27}, {15, 30}, {16, 17}, {16, 22}, {16, 23}, {16, 24}, {16, 25}, {16, 27}, {17, 18}, {17, 20}, {17, 23}, {18, 20}, {18, 23}, {18, 25}, {18, 27}, {18, 30}, {19, 24}, {19, 26}, {19, 28}, {19, 29}, {19, 31}, {19, 32}, {20, 23}, {20, 30}, {21, 22}, {21, 26}, {21, 28}, {21, 29}, {21, 33}, {22, 24}, {22, 25}, {22, 31}, {22, 32}, {22, 33}, {24, 25}, {24, 28}, {24, 29}, {24, 31}, {24, 32}, {24, 33}, {25, 27}, {25, 30}, {26, 28}, {26, 29}, {26, 31}, {27, 30}, {28, 29}, {28, 31}, {29, 33}, {31, 32}, {32, 33}}'

def make_graph(graph, img_name):
    patern = re.compile('(\\d+)')
    numbers = patern.findall(graph)
    vertices = list(map(int, set(numbers)))
    vertices.sort()
    

    g = Graph(directed=False)
    g.add_vertex(vertices[-1])

    #get only things of the form "{number  number}" where anything can be between number
    patern2 = re.compile('(\{\\d+.*?\\d+\})')

    #convert graph string to form [ ['1', '5'], ['3', '7'] ]
    edges = map(patern.findall, patern2.findall(graph[1:-1]))
    for edge in edges:
        e = g.add_edge(int(edge[0])-1, int(edge[1])-1)

    #make graph image
    graph_draw(
        g,
        vertex_text=g.vertex_index, 
        vertex_font_size=18,
        output_size=(500, 500), 
        output=img_name)




##################--------- DRIVER CODE  -------###################### 

if __name__ != '__main__':
    print('Please run as a self-conatined program')
else:
    print("Hello world, I am main.")
    make_graph(edgesOfGraph2, "edgesOfGraph2.png")
