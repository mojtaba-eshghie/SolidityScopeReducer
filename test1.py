import re


def find_function_definitions(solidity_code):
    # Define the regex pattern to match function definitions and declarations
    # This pattern looks for the 'function' keyword followed by the function name, possibly parameters, and the function body/declaration end
    pattern = r'function\s+(\w+)\s*\([^\)]*\)\s*(.*?)(\{|;|\n)'

    # Find all matches in the solidity code, but skip comments
    matches = re.finditer(pattern, solidity_code, re.MULTILINE)

    function_lines = {}
    for match in matches:
        function_name = match.group(1)
        function_declaration_end = match.group(3).strip()
        start_pos = match.start()
        end_pos = match.end()

        # Find the line number of the start position
        start_line = solidity_code.count(
            '\n', 0, start_pos) + 1  # +1 for 1-based indexing

        # Determine if the function is just declared (ends with ';') or defined (has a body with '{')
        if function_declaration_end == ';':
            # For functions that are just declared, the start and end lines are the same
            end_line = start_line
        else:
            # Find the opening brace position for the function (assuming that it's on the same line as the declaration)
            opening_brace_pos = solidity_code.find('{', end_pos)
            open_braces = 1  # Start with the opening brace of the function
            current_pos = opening_brace_pos + 1

            # Search for the matching closing brace, but skip comments
            while open_braces != 0 and current_pos < len(solidity_code):
                if solidity_code[current_pos] == '{':
                    open_braces += 1
                elif solidity_code[current_pos] == '}':
                    open_braces -= 1
                # Skip single-line comments
                elif solidity_code[current_pos:current_pos+2] == '//':
                    current_pos = solidity_code.find('\n', current_pos) + 1
                # Skip multi-line comments
                elif solidity_code[current_pos:current_pos+2] == '/*':
                    current_pos = solidity_code.find('*/', current_pos) + 2
                else:
                    current_pos += 1

            # Find the line number of the end position
            end_line = solidity_code.count('\n', 0, current_pos) + 1

        # Add the function name and its line numbers to the dictionary
        function_lines[function_name] = (start_line, end_line)

    return function_lines


def find_contract_definitions(solidity_code):
    # Define the regex pattern to match contract, interface, and abstract contract definitions
    # Updated pattern to capture contract, interface, and abstract contract names
    pattern = r'(contract|interface|abstract\s+contract)\s+(\w+)'

    # Find all matches in the solidity code, but skip comments
    matches = re.finditer(pattern, solidity_code, re.MULTILINE)

    contract_lines = {}
    for match in matches:
        contract_type = match.group(1)
        contract_name = match.group(2)
        start_pos = match.start()
        end_pos = match.end()

        # Find the line number of the start position
        start_line = solidity_code.count(
            '\n', 0, start_pos) + 1  # +1 for 1-based indexing

        # Find the opening brace position for the contract/interface/abstract contract
        opening_brace_pos = solidity_code.find('{', end_pos)
        open_braces = 1  # Start with the opening brace of the contract/interface/abstract contract
        current_pos = opening_brace_pos + 1

        # Search for the matching closing brace, but skip comments
        while open_braces != 0 and current_pos < len(solidity_code):
            if solidity_code[current_pos] == '{':
                open_braces += 1
            elif solidity_code[current_pos] == '}':
                open_braces -= 1
            # Skip single-line comments
            elif solidity_code[current_pos:current_pos+2] == '//':
                current_pos = solidity_code.find('\n', current_pos) + 1
            # Skip multi-line comments
            elif solidity_code[current_pos:current_pos+2] == '/*':
                current_pos = solidity_code.find('*/', current_pos) + 2
            else:
                current_pos += 1

        # Find the line number of the end position
        end_line = solidity_code.count('\n', 0, current_pos) + 1

        # Add the contract/interface/abstract contract name and its line numbers to the dictionary
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


# Define test cases
test_cases = [
    {
        'test_id': 1,
        'start_line': 10,
        'end_line': 10
    },
    {
        'test_id': 2,
        'start_line': 9,
        'end_line': 11
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


print(contract_definitions)
print(function_definitions)
# Run the tests
run_tests()
