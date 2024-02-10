import re


def find_function_definitions(solidity_code):
    # Define the regex pattern to match function definitions and declarations
    # This pattern looks for the 'function' keyword followed by the function name, possibly parameters, and the function body/declaration end
    pattern = r'function\s+(\w+)\s*\([^\)]*\)\s*(.*?)(\{|;|\n)'

    # Find all matches in the solidity code
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
    # Define the regex pattern to match contract, interface, and abstract contract definitions
    # Updated pattern to capture contract, interface, and abstract contract names
    pattern = r'(contract|interface|abstract\s+contract)\s+(\w+)'

    # Find all matches in the solidity code
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

        # Search for the matching closing brace
        while open_braces != 0 and current_pos < len(solidity_code):
            if solidity_code[current_pos] == '{':
                open_braces += 1
            elif solidity_code[current_pos] == '}':
                open_braces -= 1
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


def extract_function_names(solidity_code):
    """
    Extracts all function names from the given Solidity smart contract code.

    Args:
        solidity_code (str): The Solidity code as a string.

    Returns:
        list: A list of function names found in the code.
    """
    pattern = r'\b(function\s+([a-zA-Z_][a-zA-Z0-9_]*)|constructor)\s*\(.*?\)'

    # Find all matches in the Solidity code
    matches = re.findall(pattern, solidity_code)

    # Extract function names and include 'constructor' keyword explicitly
    # The regex match returns a tuple because of the group, so we process the results accordingly
    function_names = [match[1] if match[1]
                      else 'constructor' for match in matches]

    return function_names


def remove_solidity_comments(source_code):
    # Regular expression for matching single line and multi-line comments
    single_line_comment = re.compile(r'//.*')
    multi_line_comment = re.compile(r'/\*[\s\S]*?\*/')

    # Process multi-line comments
    def replacer(match):
        # Replace everything inside the comment with an equivalent number of new lines
        return '\n' * match.group(0).count('\n')

    # Replace multi-line comments with newlines to preserve line numbers
    no_multi_line_comments = re.sub(multi_line_comment, replacer, source_code)

    # Process each line to remove single-line comments
    lines = no_multi_line_comments.split('\n')
    for i, line in enumerate(lines):
        if '//' in line:
            lines[i] = re.sub(single_line_comment, '', line)

    # Join the processed lines back into a single string
    processed_code = '\n'.join(lines)

    return processed_code


def replace_contract_bodies_with_newlines(solidity_code):
    # Regular expression to match contract declaration lines
    contract_pattern = re.compile(r'\bcontract\s+\w+')
    # Initialize a list to hold the processed lines
    processed_lines = []
    # Stack to track open braces
    brace_stack = []
    # Flag to track whether we're inside a contract body
    inside_contract = False

    # Split the code into lines for processing
    lines = solidity_code.split('\n')

    for line in lines:
        # Check if the line declares a contract
        if contract_pattern.search(line):
            inside_contract = True
            brace_stack.append('{')
            # Add the contract declaration line as is
            processed_lines.append(line)
            continue

        if inside_contract:
            # Count opening and closing braces
            open_braces = line.count('{')
            close_braces = line.count('}')
            # Add to stack for every open brace
            brace_stack.extend(['{'] * open_braces)
            # Pop from stack for every close brace
            for _ in range(close_braces):
                if brace_stack:
                    brace_stack.pop()

            if not brace_stack:  # If the stack is empty, we've exited the contract body
                inside_contract = False

            # Replace the line with a newline if inside the contract, except for the closing brace line
            processed_lines.append('' if brace_stack else line)
        else:
            # Add lines outside of contracts as is
            processed_lines.append(line)

    return '\n'.join(processed_lines)


def replace_function_bodies_with_newlines(solidity_code):
    # Regular expression to match function declarations
    function_pattern = re.compile(r'\bfunction\s+\w+')
    # Initialize a list to hold the processed lines
    processed_lines = []
    # Stack to track open braces for functions
    brace_stack = []
    # Flag to track whether we're inside a function body
    inside_function = False

    # Split the code into lines for processing
    lines = solidity_code.split('\n')

    for line in lines:
        # Check if the line declares a function
        if function_pattern.search(line):
            inside_function = True
            brace_stack.append('{')
            # Add the function declaration line as is
            processed_lines.append(line)
            continue

        if inside_function:
            # Count opening and closing braces
            open_braces = line.count('{')
            close_braces = line.count('}')
            # Add to stack for every open brace
            brace_stack.extend(['{'] * open_braces)
            # Pop from stack for every close brace
            for _ in range(close_braces):
                if brace_stack:
                    brace_stack.pop()
                if not brace_stack:  # If the stack is empty, we've exited the function body
                    inside_function = False
                    # Include the closing brace line
                    processed_lines.append(line)
                    break

            # Replace the line with a newline if inside the function, except for the closing brace line
            if inside_function or brace_stack:
                processed_lines.append('')
        else:
            # Add lines outside of functions as is
            processed_lines.append(line)

    return '\n'.join(processed_lines)


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
    },
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


solidity_code = open('sample1.sol', 'r').read()
uncommented_solidity_code = remove_solidity_comments(solidity_code)
function_names = extract_function_names(uncommented_solidity_code)
contract_definitions = find_contract_definitions(uncommented_solidity_code)
function_definitions = find_function_definitions(uncommented_solidity_code)


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
