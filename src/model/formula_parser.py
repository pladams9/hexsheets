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

    @staticmethod
    def _tokenize(string):
        operators = ['+', '-', '*', '/']
        brackets = {
            '"': '"',
            '(': ')',
            '[': ']'
        }

        tokens = []
        sub_start = 0
        current_bracket = None
        for index, char in enumerate(string):
            if current_bracket:
                if char == brackets[current_bracket]:
                    tokens.append(('BRACKET', current_bracket, string[sub_start:index].strip()))
                    current_bracket = None
                    sub_start = index + 1
                continue

            if char in brackets:
                current_bracket = char
                value = string[sub_start:index].strip()
                if value != '':
                    tokens.append(('VALUE', value))
                sub_start = index + 1
            elif char in operators:
                value = string[sub_start:index].strip()
                if value != '':
                    tokens.append(('VALUE', value))
                tokens.append(('OPERATOR', char))
                sub_start = index + 1
        else:
            value = string[sub_start:].strip()
            if value != '':
                tokens.append(('VALUE', value))

        return tokens

    def _parse_formula(self, formula):
        tokens = self._tokenize(formula)
        values_and_operators = []
        for token in tokens:
            if token[0] == 'VALUE':
                values_and_operators.append(('VALUE', self._cast_value(token[1])))
            elif token[0] == 'OPERATOR':
                values_and_operators.append(token)
            elif token[0] == 'BRACKET':
                if token[1] == '"':
                    values_and_operators.append(('VALUE', token[2]))
                elif token[1] == '(':
                    values_and_operators.append(('VALUE', self._parse_formula(token[2])))
                elif token[1] == '[':
                    address = self._parse_address(token[2])
                    values_and_operators.append(('VALUE', self._parse_formula(self._nodes[address])))

        if len(values_and_operators) < 1 or values_and_operators[0][0] != 'VALUE':
            return '#ERROR'
        else:
            return_value = values_and_operators.pop(0)[1]
            while len(values_and_operators) > 0:
                operator = values_and_operators.pop(0)[1]
                if operator == '+':
                    return_value += values_and_operators.pop(0)[1]
                elif operator == '-':
                    return_value -= values_and_operators.pop(0)[1]
                elif operator == '*':
                    return_value *= values_and_operators.pop(0)[1]
                elif operator == '/':
                    return_value /= values_and_operators.pop(0)[1]
        return return_value

    def _parse_address(self, address):
        if address.count(',') != 1:
            return -1, -1

        coordinates = address.split(',')

        for i in range(2):
            coordinates[i] = self._parse_formula(coordinates[i])
            if not isinstance(coordinates[i], int):
                return -1, -1
        return tuple(coordinates)

    @staticmethod
    def _cast_value(value):
        if (value.replace('.', '').replace('-', '').isdigit()) and value.count('.') <= 1:
            if value.count('.') == 1:
                return float(value)
            else:
                return int(value)
        else:
            return value
