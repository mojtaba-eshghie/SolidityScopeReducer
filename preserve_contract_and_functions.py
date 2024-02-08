import re


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


source_code = open('sample3_uncommented.sol', 'r').read()


processed_code = replace_contract_bodies_with_newlines(source_code)
# Display or save the processed code
print(processed_code)
output = open('sample3_removed.sol', 'w').write(processed_code)
