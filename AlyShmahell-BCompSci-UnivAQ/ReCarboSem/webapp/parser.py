import re

def parser(graph):
    pairs = []
    types = {}
    for node in graph:
        if not "targets" in node:
            continue
        for target in node["targets"]:
            pairs += [
                [
                    node['title'],
                    graph[target['target']]['title']
                ]
            ]
            types[f"{node['title']}{graph[target['target']]['title']}"] = target['type']
    nodes = []
    for pair in pairs:
        nodes += pair
    nodes = list(set(nodes))
    links = [
        {
            "source": nodes.index(pair[0]),
            "target": nodes.index(pair[1]),
            "type": types[f"{pair[0]}{pair[1]}"]
        }
        for pair in pairs
    ]
    nodes = [
        {'id': node}
        for node in nodes
    ]
    roots = list(set([
        re.sub(r'[0-9]+', '', node['id'])
        for node in nodes
    ]))
    types = list(set([link['type'] for link in links]))
    return {
        "nodes": nodes,
        "links": links,
        "types": types,
        "roots": roots
    }

if __name__ == '__main__':
    import sys
    import json
    with open(sys.argv[1], 'r') as f:
        graph = json.load(f)
    res = parser(graph['nodes'])
    with open('temp.json', 'w') as f:
        json.dump(res, f, ensure_ascii=False, indent=4)