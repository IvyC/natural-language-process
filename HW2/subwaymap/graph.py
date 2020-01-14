# coding:utf-8
import json
import networkx as nx
import matplotlib.pyplot as plt
import math
from matplotlib.font_manager import _rebuild

_rebuild()

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

with open('data/北京市地铁.json', 'r') as load_f:
    load_dict = json.load(load_f)

result = {}
transferSet = set()

for ele in (load_dict['l']):
    st_list = ele['st']
    for st in st_list:
        x_y = (st['p']['x'], st['p']['y'])
        result[st['name']] = x_y
        if st['strans']:
            transferSet.add(st['name'])

# sub_graph = nx.Graph()

# sub_graph.add_nodes_from(list(result.keys()))

# nx.draw(sub_graph, result, with_labels=True, node_size=10, font_family='SimHei')

# plt.show()

def geo_distance(origin, destination):
    x1, y1 = origin
    x2, y2 = destination
    distance = math.sqrt(math.pow((x1 - x2), 2) + math.pow((y1 - y2), 2))
    return distance


def get_st_distance(st1, st2):
    return geo_distance(result[st1], result[st2])


from collections import defaultdict


def build_connection():
    stations_connection = defaultdict(list)
    station = list(result.keys())
    for st1 in station:
        for ele in (load_dict['l']):
            st_list = ele['st']
            for i in range(len(st_list)):
                if st1 == st_list[i]['name']:
                    if (i - 1) >= 0:
                        stations_connection[st1].append(st_list[i - 1]['name'])
                    if (i + 1) < len(st_list):
                        stations_connection[st1].append(st_list[i + 1]['name'])
    return stations_connection


st_connections = build_connection()

st_connection_graph = nx.Graph(st_connections)
nx.draw(st_connection_graph, result, with_labels=True, node_size=5)

plt.show()

def isTransfer(station):
    if station in transferSet:
        return True
    else:
        return False

def get_distance_of_path(path):
    distance = 0
    for i, _ in enumerate(path[:-1]):
        distance += get_st_distance(path[i], path[i+1])
    return distance


def get_transfer_of_path(path):
    transfer = 0
    for i in range(len(path)):
        if isTransfer(path[i]):
            transfer += 1
    return transfer

def get_combo_of_path(path):
    path_distance = math.log10(get_distance_of_path(path))
    path_transfer = get_transfer_of_path(path)
    gradient = math.sqrt(math.pow(path_distance, 2) + math.pow(path_transfer, 2))
    return gradient

def sort_by_distance(paths):
    return sorted(paths, key=get_distance_of_path)

def sorted_by_transfer(paths):
    return sorted(paths, key=get_transfer_of_path)

def sorted_by_combo(paths):
    return sorted(paths, key=get_combo_of_path)

## find the shortest path by BFS
def BFS(graph, start, end, search_strategy):
    paths = [[start]]
    visited = set()

    while paths:
        path = paths.pop(0)
        froniter = path[-1]

        if froniter in visited: continue
        if froniter == end:
            print(path)
            return path

        successors = graph[froniter]

        for station in successors:
            if station in path: continue

            new_path = path + [station]
            paths.append(new_path)

            paths = search_strategy(paths)
        visited.add(froniter)

def search(start, end, search_strategy):
    return BFS(st_connections, start, end, search_strategy)