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
        brackets = []
        bracket_pairs = []
        for index, char in enumerate(formula):
            if char == '[':
                brackets.append(index)
            if char == ']':
                bracket_pairs.insert(0, (brackets.pop(), index))
        for bracket_pair in bracket_pairs:
            coordinates = tuple([int(x) for x in formula[bracket_pair[0] + 1:bracket_pair[1]].split(',')])
            cell_value = self.get_node_value(coordinates)
            formula = formula[0:bracket_pair[0]] + str(cell_value) + formula[bracket_pair[1] + 1:]

        operators = ['+', '-']
        formula = formula.replace(' ', '')

        sum = 0
        current_operand = ''
        last_operator = ''
        while len(formula) > 0:
            char = formula[0]
            formula = formula[1:]

            if char in operators:
                if last_operator == '':
                    sum = self._cast_value(current_operand)
                elif last_operator == '+':
                    sum += self._cast_value(current_operand)
                elif last_operator == '-':
                    sum -= self._cast_value(current_operand)

                current_operand = ''
                last_operator = char
            else:
                current_operand = current_operand + char
        else:
            if last_operator == '':
                sum = self._cast_value(current_operand)
            elif last_operator == '+':
                sum += self._cast_value(current_operand)
            elif last_operator == '-':
                sum -= self._cast_value(current_operand)

        return sum

    @staticmethod
    def _cast_value(value):
        if (value.replace('.', '').replace('-', '').isdigit()) and value.count('.') <= 1:
            if value.count('.') == 1:
                return float(value)
            else:
                return int(value)
        else:
            return value
