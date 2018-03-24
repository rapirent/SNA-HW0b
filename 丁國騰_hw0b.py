from queue import PriorityQueue
from sys import stdin
import re


INF = 2147483647

def stack(cur, start, table, route, graph, output):
    if cur == start:
        print(table[cur], end='', file=output)
        return
    stack(route[cur], start, table, route, graph, output)
    print('--' +str(graph[route[cur]][cur]), end='', file=output)
    print('--' + table[cur], end='', file=output)


def dijkstra(source, target, graph, table):
    dis = {key: INF for key in table.keys()}
    route = {key: key for key in table.keys()}
    dis[source] = 0
    pq = PriorityQueue()
    pq.put([0, source])
    while not pq.empty():
        edge = pq.get()
        if dis[edge[1]] < edge[0]:
            continue
        if edge[1] not in graph:
            continue
        for i in graph[edge[1]]:
            if dis[i] > (dis[edge[1]] + graph[edge[1]][i]):
                dis[i] = dis[edge[1]] + graph[edge[1]][i]
                route[i] = edge[1]
                pq.put([dis[i], i])

    return (dis[target], route)

if __name__ == '__main__':
    nodes_file = open('movie_nodes.txt', 'r')
    name_table = dict()
    id_table = dict()
    for line in nodes_file:
        parse = [t(s) for t, s in zip((int, str), re.search('^(\d+)\t(.+)\n$', line).groups())]
        name_table[parse[1]] = parse[0]
        id_table[parse[0]] = parse[1]

    edges_file = open('movie_edgesw.txt', 'r')
    # it can also be a 2 dimentional list,
    # but we don't know whether a input file a continue number
    graph = dict()
    for line in edges_file:
        parse = [t(s) for t, s in zip((int, int, float), re.search('^(\d+)\t(\d+)\t([\d.]+)\n$', line).groups())]
        if parse[0] not in graph:
            graph[parse[0]] = {}
        if parse[1] not in graph:
            graph[parse[1]] = {}
        graph[parse[0]][parse[1]] = graph[parse[1]][parse[0]] = parse[2]

    nodes_file.close()
    edges_file.close()
    output = open('丁國騰_hw0b.txt', 'w')
    line = input('please input the source name:')
    while line:
        source = line
        line = input('please input the target name:')
        if not line:
            break
        target = line
        (distance, route_list) = dijkstra(name_table[source], name_table[target], graph, id_table)
        print('distance = ' + str(distance), file=output)
        stack(name_table[target], name_table[source], id_table, route_list, graph, output)
        print('', file=output)
        line = input('please input the source name:')

    output.close()
