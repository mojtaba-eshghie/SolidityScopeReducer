def find_enclosing_contract(file_path, start_line, end_line):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    contracts = []
    contract_stack = []

    # Find contracts and their boundaries
    for i, line in enumerate(lines):
        if line.strip().startswith('contract '):
            contract_name = line.strip().split(' ')[1].split('{')[0]
            contract_stack.append({'name': contract_name, 'start': i + 1})

        if '{' in line and contract_stack:
            contract_stack[-1]['braces_count'] = contract_stack[-1].get(
                'braces_count', 0) + line.count('{')

        if '}' in line and contract_stack:
            contract_stack[-1]['braces_count'] -= line.count('}')

            if contract_stack[-1]['braces_count'] == 0:
                contract = contract_stack.pop()
                contract['end'] = i + 1
                contracts.append(contract)

    # Check if the given code chunk is within any contract
    for contract in contracts:
        if contract['start'] <= start_line and contract['end'] >= end_line:
            return contract['name']

    return None


# Usage
file_path = 'sample.sol'


# Define test cases
test_cases = [
    {
        'test_id': 1,
        'start_line': 10,
        'end_line': 12
    },
    {
        'test_id': 2,
        'start_line': 1,
        'end_line': 8
    },
    {
        'test_id': 3,
        'start_line': 70,
        'end_line': 73
    },
    {
        'test_id': 4,
        'start_line': 115,
        'end_line': 117
    },
    {
        'test_id': 5,
        'start_line': 1,
        'end_line': 4
    },
    {
        'test_id': 6,
        'start_line': 5,
        'end_line': 35
    },
    {
        'test_id': 7,
        'start_line': 5,
        'end_line': 25
    },
    {
        'test_id': 8,
        'start_line': 1,
        'end_line': 1
    },
    {
        'test_id': 9,
        'start_line': 111,
        'end_line': 111
    },
    {
        'test_id': 10,
        'start_line': 100,
        'end_line': 110
    },
    {
        'test_id': 11,
        'start_line': 10,
        'end_line': 110
    }
]

# Function to run tests


def run_tests():
    for i, test in enumerate(test_cases):
        print(
            '- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
        try:
            result = find_enclosing_contract(
                file_path, test['start_line'], test['end_line'])
            print(
                f"Result for test #{test['test_id']} ({test['start_line']}, {test['end_line']}) : {result}")
        except Exception as e:
            print(f"Error: {e}")


# Run the tests
run_tests()
