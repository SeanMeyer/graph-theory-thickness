#Import all of the graphs from the competition.
from competitionGraphs2018 import *

#Import graph tool into the main namespace
from graph_tool.all import *
import re
import random

def make_graph(graph):
    graph = graph.replace('\n', '')
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

    return g

#make graph image
def draw_graph_png(g, img_name):
    if is_planar(g):
        pos = planar_layout(g)
    else:
        pos = None
    graph_draw(
        g,
        vertex_text=g.vertex_index, 
        vertex_font_size=18,
        output_size=(500, 500), 
        output=img_name,
        pos=pos)


##################--------- Maximal Subgraph  -------######################
def random_edge_filter(graph):
    # Create subgraph
    subgraph = GraphView(graph)

    # Get random edge
    edges = list(subgraph.edges())
    e = random.choice(edges)

    # Filter subgraph
    gprop_bool = subgraph.new_edge_property("bool")
    gprop_bool.a = False 
    gprop_bool[e] = True
    return gprop_bool


def mps_naive(graph, filter=None):
    if filter is None:
        filter = random_edge_filter(graph)
    # Create subgraph using filter
    subgraph = GraphView(graph, efilt=filter)

    # Create subgraph of inverted filter
    opp_graph = GraphView(graph)
    opp_graph.set_edge_filter(filter, inverted=True)
    edge_list = list(opp_graph.edges())
    random.shuffle(edge_list)

    # Loop through remaining edges, adding to subgraph
    for e in edge_list:
        # Add edge
        filter[e] = True
        subgraph.set_edge_filter(filter)
        # Check planarity and remove edge if not planar
        if not is_planar(subgraph):
            filter[e] = False
            subgraph.set_edge_filter(filter)
    return subgraph

def mps_naive_best(graph, count, filter=None):
    best = 0
    for i in range(count):
        sg = mps_naive(graph, filter)
        edge_count = sg.num_edges()
        if edge_count > best:
            best = edge_count
            best_sg = sg
    return best_sg

def thickness(graph):
    t = 1
    remaining = graph.copy()
    while not is_planar(remaining):
        t += 1
        mps = mps_naive_best(remaining, 1)
        remaining.set_edge_filter(mps.get_edge_filter()[0], inverted=True)
        remaining.purge_edges()
        edges = remaining.get_edges()
        remaining = Graph(directed=False)
        remaining.add_edge_list(edges)
    return t

##################--------- DRIVER CODE  -------###################### 

if __name__ != '__main__':
    print('Please run as a self-conatined program')
else:
    print("Making edgesOfGraph2.png.")
    draw_graph_png(make_graph(edgesOfGraph2), "edgesOfGraph2.png")