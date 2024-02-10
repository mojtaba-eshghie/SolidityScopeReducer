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


def find_function_definitions2(solidity_code):
    # Matches function definitions, capturing the opening brace if present
    pattern = r'function\s+(\w+)\s*\([^\)]*\)\s*(public|private|internal|external)?\s*(returns\s*\([^\)]*\))?\s*({)?'

    matches = re.finditer(pattern, solidity_code, re.DOTALL | re.MULTILINE)

    function_lines = {}
    for match in matches:
        function_name = match.group(1)
        # Checks if the function declaration ends with an opening brace
        has_body = match.group(4) == '{'

        start_pos = match.start()
        start_line = solidity_code.count('\n', 0, start_pos) + 1

        if has_body:
            open_braces = 1  # We start with one open brace
            current_pos = match.end()

            while open_braces > 0 and current_pos < len(solidity_code):
                if solidity_code[current_pos] == '{':
                    open_braces += 1
                elif solidity_code[current_pos] == '}':
                    open_braces -= 1
                current_pos += 1

            end_line = solidity_code.count('\n', 0, current_pos)
        else:
            # If the function is a declaration or the body is not detected, set the end line same as start line
            end_line = start_line

        function_lines[function_name] = (start_line, end_line)

    return function_lines


solidity_code = open('sample3_uncommented.sol', 'r').read()
function_definitions = find_function_definitions2(solidity_code)
print(function_definitions)
