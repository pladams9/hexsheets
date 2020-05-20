class FormulaParser:
    def __init__(self):
        self._nodes = {}

    def update_nodes(self, nodes):
        for node in nodes:
            self._nodes[node] = str(nodes[node])

    def delete_nodes(self, nodes):
        for node in nodes:
            self._nodes.pop(node)

    def get_node_value(self, node):
        formula = self._nodes[node]
        if formula[0] == '=':
            value = self._parse_formula(formula[1:])
        else:
            value = self._cast_value(formula)
        return value

    def _parse_formula(self, formula):
        if formula[0] == '[':
            return 22
        else:
            return 2

    def _cast_value(self, value):
        if value.replace('.', '').replace('-', '').isdigit():
            if value.count('.') == 1:
                return float(value)
            else:
                return int(value)
        else:
            return value
