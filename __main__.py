    
#Import all of the graphs from the competition.
from competitionGraphs2018 import *
from ks import *

#Import graph tool into the main namespace
from graph_tool.all import *
import re
import random
import math
import time

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
    planar_graphs = []
    remaining = graph.copy()
    while not is_planar(remaining):
        mps = mps_naive_best(remaining, 1)
        edges = mps.get_edges()
        add_graph = Graph(directed=False)
        add_graph.add_edge_list(edges)
        planar_graphs.append(add_graph)
        remaining.set_edge_filter(mps.get_edge_filter()[0], inverted=True)
        remaining.purge_edges()
        edges = remaining.get_edges()
        remaining = Graph(directed=False)
        remaining.add_edge_list(edges)
    planar_graphs.append(remaining)
    return planar_graphs

def best_thickness(graph, runs):
    bestValue = math.inf
    planar_graphs = []
    for _ in range(runs):
        result = thickness(graph)
        thickVal = len(result)
        if (thickVal < bestValue):
            bestValue = thickVal
            planar_graphs = result
    return planar_graphs

def find_thickness_two(graph, max_minutes, until=2):
    bestEdgeCount = math.inf
    until += 1
    thickVal = until
    planar_graphs = []
    t_end = time.time() + 60 * max_minutes
    while (thickVal >= until and time.time() < t_end):
        result = thickness(graph)
        lastGraph = result[-1]
        lastGraphEdgeCount = lastGraph.num_edges()
        thickVal = len(result)
        if (thickVal < until or lastGraphEdgeCount < bestEdgeCount):
            planar_graphs = result
    return planar_graphs

def save_best_runs(graph_name, runs):
    graph = make_graph(graph_names[graph_name])
    planar_graphs = best_thickness(graph, runs)
    save_graphs(planar_graphs, graph_name)
    return

def save_best_time(graph_name, max_minutes, alternate_graph=None, until=2):
    if alternate_graph is None:
        graph = make_graph(graph_names[graph_name])
    else:
        graph = complete_graph(alternate_graph)
    planar_graphs = find_thickness_two(graph, max_minutes, until=until)
    save_graphs(planar_graphs, graph_name)
    return

def save_graphs(graphs, filename_prefix):
    i = 1
    for g in graphs:
        g.save(filename_prefix+"-"+str(i)+".graphml", "graphml")
        i += 1

def max_degree(graph):
    d = []
    for v in graph.vertices():
        d.append(v.out_degree())
    return max(d)

def hilight_subs(graph_name):
    graph = make_graph(graph_names[graph_name])
    from numpy.random import poisson
    vm = gt.subgraph_isomorphism(k5, graph, max_n=500)
    for i in range(len(vm)):
        graph.set_vertex_filter(None)
        graph.set_edge_filter(None)
        vmask, emask = mark_subgraph(graph, k5, vm[i])
        graph.set_vertex_filter(vmask)
        graph.set_edge_filter(emask)
        assert gt.isomorphism(g, sub)
    graph.set_vertex_filter(None)
    graph.set_edge_filter(None)
    ewidth = g.copy_property(emask, value_type="double")
    ewidth.a += 0.5
    ewidth.a *= 2
    graph_draw(g, vertex_fill_color=vmask, edge_color=emask,
        edge_pen_width=ewidth, output_size=(200, 200),
        output="subgraph-iso-embed.pdf")
    #g.save(graph_name+".graphml", "graphml")

##################--------- DRIVER CODE  -------###################### 

if __name__ != '__main__':
    print('Please run as a self-conatined program')
else:
    print("Making edgesOfGraph2.png.")
    #draw_graph_png(make_graph(edgesOfGraph2), "edgesOfGraph2.png")