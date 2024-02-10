import re


def find_function_definitions(solidity_code):
    # Define the regex pattern to match function definitions
    # This pattern looks for the 'function' keyword followed by the function name and possibly parameters
    pattern = r'function\s+(\w+)\s*\('

    # Find all matches in the solidity code
    matches = re.finditer(pattern, solidity_code, re.MULTILINE)

    function_lines = {}
    for match in matches:
        function_name = match.group(1)
        start_pos = match.start()
        end_pos = match.end()

        # Find the line number of the start position
        start_line = solidity_code.count(
            '\n', 0, start_pos) + 1  # +1 for 1-based indexing

        # Find the opening brace position for the function (assuming that it's on the same line as the declaration)
        opening_brace_pos = solidity_code.find('{', end_pos)
        open_braces = 1  # Start with the opening brace of the function
        current_pos = opening_brace_pos + 1

        # Search for the matching closing brace
        while open_braces != 0 and current_pos < len(solidity_code):
            if solidity_code[current_pos] == '{':
                open_braces += 1
            elif solidity_code[current_pos] == '}':
                open_braces -= 1
            current_pos += 1

        # Find the line number of the end position
        end_line = solidity_code.count('\n', 0, current_pos) + 1

        # Add the function name and its line numbers to the dictionary
        function_lines[function_name] = (start_line, end_line)

    return function_lines


def find_contract_definitions(solidity_code):
    # Define the regex pattern to match contract definitions
    # Modified pattern to capture the contract name
    pattern = r'contract\s+(\w+)'

    # Find all matches in the solidity code
    matches = re.finditer(pattern, solidity_code, re.MULTILINE)

    contract_lines = {}
    for match in matches:
        contract_name = match.group(1)
        start_pos = match.start()
        end_pos = match.end()

        # Find the line number of the start position
        start_line = solidity_code.count(
            '\n', 0, start_pos) + 1  # +1 for 1-based indexing

        # Find the opening brace position for the contract
        opening_brace_pos = solidity_code.find('{', end_pos)
        open_braces = 1  # Start with the opening brace of the contract
        current_pos = opening_brace_pos + 1

        # Search for the matching closing brace
        while open_braces != 0 and current_pos < len(solidity_code):
            if solidity_code[current_pos] == '{':
                open_braces += 1
            elif solidity_code[current_pos] == '}':
                open_braces -= 1
            current_pos += 1

        # Find the line number of the end position
        end_line = solidity_code.count('\n', 0, current_pos) + 1

        # Add the contract name and its line numbers to the dictionary
        contract_lines[contract_name] = (start_line, end_line)

    return contract_lines


def chunk_locator(solidity_code, start, end, contract_definitions, function_definitions):
    contract_name = None
    function_name = None

    for contract in contract_definitions:
        if (start >= contract_definitions[contract][0]) and (end <= contract_definitions[contract][1]):
            contract_name = contract
            break

    for function in function_definitions:
        if (start >= function_definitions[function][0]) and (end <= function_definitions[function][1]):
            function_name = function

    return {
        "function_name": function_name,
        "contract_name": contract_name
    }


solidity_code = open('sample1.sol', 'r').read()
contract_definitions = find_contract_definitions(solidity_code)
function_definitions = find_function_definitions(solidity_code)

# print(chunk_locator(solidity_code, 25, 26, contract_definitions, function_definitions))


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


def run_tests():
    for i, test in enumerate(test_cases):
        print(
            '- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
        try:
            result = chunk_locator(
                solidity_code, test['start_line'], test['end_line'], contract_definitions, function_definitions)
            if result is None:
                print(
                    f"Result for test #{test['test_id']} ({test['start_line']}, {test['end_line']}) : {result}")
            else:
                print(
                    f"Result for test #{test['test_id']} ({test['start_line']}, {test['end_line']}) : {result}")
        except Exception as e:
            print(f"Error: {e}")


# Run the tests
run_tests()
