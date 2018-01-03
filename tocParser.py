from __future__ import print_function
import json
import sys


def tocParser(inputFile):
    dataFile = open(inputFile)
    # Convert JSON tree to a Python dict
    data = json.load(dataFile)

    # Convert back to JSON & print to stderr so we can verfiy that the tree is correct.
    # print(json.dumps(data, indent=4), file=sys.stderr)

    treedict = data
    # Extract tree edges from the dict
    edges = []

    def get_edges(treedict, parent=None):
        print(treedict)
        name = next(iter(treedict.keys()))
        if parent is not None:
            edges.append((parent, name))
        for item in treedict[name]["children"]:
            if isinstance(item, dict):
                get_edges(item, parent=name)
            else:
                edges.append((name, item))

    get_edges(data)

    # Dump edge list in Graphviz DOT format
    print('strict digraph tree {')
    for row in edges:
        print('    {0} -> {1};'.format(*row))
    print('}')

# python tree_to_graph.py | dot -Tpng -otree.png

tocParser("toc-8-3.json")