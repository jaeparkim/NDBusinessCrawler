import json
import networkx as nx
import matplotlib.pyplot as plt
import random
from datetime import datetime


def construct_graph(data):
    graph = nx.Graph()

    business_entity = ['Commercial Registered Agent', 'Registered Agent', 'Owners']
    color = {
        'Commercial Registered Agent': 'red',
        'Registered Agent': 'green',
        'Owners': 'blue'
        }

    for item in data:
        business_name = item['business_name'][0].split('\n')[0]
        for entity in business_entity:
            try:
                business_ownername = item['filing_detail'][entity].split('\n')[0] # data entry might be blank
                graph.add_node(business_name, color='dimgray')
                graph.add_node(business_ownername, color=color[entity])
                graph.add_edge(business_name, business_ownername)
            except:
                pass

    return graph


def plot_graph(graph):
    color_map = []
    for n in graph.nodes():
        color_map.append(graph.nodes[n]['color'])

    pos = nx.nx_agraph.graphviz_layout(graph, prog="neato")

    nx.draw_networkx(graph, pos, node_color=color_map, with_labels=False, node_size=10)

    plt.title('Business in North Dakota whose name starts with \'X\'')
    plt.savefig('../NorthDakotaBusinesses.png', bbox_inches='tight')
    plt.close()


if __name__ == '__main__':
    with open('../business_data.json', 'r') as f:
        data = json.load(f)
    
    graph = construct_graph(data)
    plot_graph(graph)

    f.close()
