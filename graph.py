from pyvis import network as pvnet
import networkx as nx
import csv

def plot_g_pyviz(G,):
    net = pvnet.Network(notebook=True, directed=True)

    net.from_nx(G)
    edges_data_set = net.get_edges()
    nodes = net.get_nodes()
    nodes_data_set = []
    for node in nodes:
        nodes_data_set.append({"id": node, "label": node.title(), "shape": "dot", "size": 10})

    return {'nodes_info': nodes_data_set, 'edges_info': edges_data_set}


def init_graph(spy_name):
    G = nx.MultiDiGraph()
    with open(f'new_result.csv', "r", newline="") as file:
            rd = {}
            reader = csv.reader(file)
            for row in reader:
                name = (row[0]+row[1]+row[2]).lower()
                search = ''.join(spy_name.lower().split())
                if name == search:
                    from_time = row[5]+row[6]
                    rd[from_time] = [r.lower() for r in row]

            for number, row in enumerate(sorted(rd.keys())):
                if (rd[row][3], rd[row][4]) in [(edge[0], edge[1]) for edge in G.edges]:
                    rad = [edge[2]['rad'] for edge in G.edges(data=True) if (edge[0], edge[1]) == (rd[row][3], rd[row][4])]
                    current_rad = max(rad) + 0.1
                    G.add_edge(rd[row][3], rd[row][4], rad=current_rad, label=number)
                else:
                    G.add_edge(rd[row][3], rd[row][4], rad=0.1, label=number)

    pos = nx.circular_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=0)
    nx.draw_networkx_labels(G, pos, font_size=15, font_color='green')
    for edge in G.edges(data=True):
        nx.draw_networkx_edges(G, pos, edgelist=[(edge[0],edge[1])], connectionstyle=f'arc3,rad={edge[2]["rad"]}', min_source_margin=8, min_target_margin=12)

    
    return G


def get_result(spy_name):
    return plot_g_pyviz(init_graph(spy_name))

