class FormulaParser:
    def __init__(self):
        self._nodes = {}

    def update_nodes(self, nodes):
        for node in nodes:
            self._nodes[node] = nodes[node]

    def delete_nodes(self, nodes):
        for node in nodes:
            self._nodes.pop(node)
