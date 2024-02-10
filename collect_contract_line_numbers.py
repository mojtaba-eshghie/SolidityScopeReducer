import re


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


# Sample solidity code
solidity_code = open('sample.sol', 'r').read()
# Get contract definition line numbers
contract_definitions = find_contract_definitions(solidity_code)
print(contract_definitions)
