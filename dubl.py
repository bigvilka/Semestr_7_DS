import csv
import networkx as nx
from datetime import datetime, timedelta



def get_dubl(flights_number, time_in_city, multidigraph_check):
    counter = {}
    flights_for_every_name = {}
    with open(f'new_result.csv', "r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                name = (row[0] + ' ' + row[1] + ' ' + row[2]).lower()
                if not row[2]:
                    name = (row[0] + ' ' + row[1]).lower()
                counter[name] = counter.get(name, 0) + 1
                from_time = row[5]+' '+row[6]
                if flights_for_every_name.get(name):
                    flights_info = flights_for_every_name[name]
                    flights_info[from_time] = [r.lower() for r in row]
                    flights_for_every_name[name] = flights_info
                else:
                    flights_for_every_name[name] = {from_time: [r.lower() for r in row]}

    filtered_names = [el for el, count in counter.items() if count > flights_number]

    tic_filtered_names = []
    mdg_filtered_names = []
    for filtered_name in filtered_names:
        G = nx.MultiDiGraph()
        rd = flights_for_every_name[filtered_name]
        for number, row in enumerate(sorted(rd.keys())):
            if (rd[row][3], rd[row][4]) in [(edge[0], edge[1]) for edge in G.edges]:
                rad = [edge[2]['rad'] for edge in G.edges(data=True) if (edge[0], edge[1]) == (rd[row][3], rd[row][4])]
                current_rad = max(rad) + 0.1
                G.add_edge(rd[row][3], rd[row][4], rad=current_rad, label=number, from_time=row)
            else:
                G.add_edge(rd[row][3], rd[row][4], rad=0.1, label=number, from_time=row)

        edges_info = G.edges(data=True)
        sorted_edges_info = sorted(edges_info, key=lambda edge: edge[2]['from_time'])

        timedelta_flag = True
        for label, edge in enumerate(sorted_edges_info):
            if label < len(sorted_edges_info) - 1:
                if edge[1] == sorted_edges_info[label + 1][0]:
                    dt_fmt = '%Y-%m-%d %H:%M'
                    dt_s1 = edge[2]['from_time']
                    dt_s2 = sorted_edges_info[label + 1][2]['from_time']

                    dt1 = datetime.strptime(dt_s1, dt_fmt)
                    dt2 = datetime.strptime(dt_s2, dt_fmt)
                    delta = dt2 - dt1
                    if int(delta.total_seconds())//3600 > time_in_city:
                        timedelta_flag = False

        if timedelta_flag:
            tic_filtered_names.append(filtered_name.title())

        multidigraph_flag = False
        if multidigraph_check:
            for edge in sorted_edges_info:
                if edge[2]['rad'] > 0.1:
                    multidigraph_flag = True

        if timedelta_flag and multidigraph_flag:
            mdg_filtered_names.append(filtered_name.title())


    if multidigraph_check:
        return mdg_filtered_names
    else:
        return tic_filtered_names