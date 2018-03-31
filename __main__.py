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

#Import all of the graphs from the competition.
from competitionGraphs2018 import *

#Import graph tool into the main namespace
from graph_tool.all import *
import re

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
    print("Making edgesOfGraph2.png.")
    make_graph(edgesOfGraph2, "edgesOfGraph2.png")