graf = [['1', '2', '6'], ['1', '3', '2'], ['1', '4', '10'], ['2', '4', '4'], ['3', '1', '5'],
        ['3', '2', '3'], ['3', '4', '8'], ['4', '2', '1']] # start end length
print(graf)

start = '1'
end = '4'

def node_1(start, graf):
    points_from_node = {}
    for i in range(0, len(graf)):
        if graf[i][0] == start:
            points_from_node[graf[i][1]] = graf[i][2]
    return points_from_node


way = []
length_way = 0
def search(start, end,  graf, response_way, way = [start], length_way = 0):
    node = node_1(start, graf)
    for i in node.keys():
        length_way += int(node[i])
        if length_way <= response_way:
            response_way = length_way
            if i == end:
                return way.append(start)
            else:
                return search(i, graf, way, length_way, response_way)

print(search(start, end, graf, way = [], length_way = 0, response_way = len(graf)*100))