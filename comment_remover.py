import re


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


# Example usage
# Update this path to your Solidity file
source_code_path = 'sample3.sol'
# Update this path to your output file
output_code_path = 'sample3_uncommented.sol'

with open(source_code_path, 'r') as file:
    source_code = file.read()

# Remove comments from the source code
processed_code = remove_solidity_comments(source_code)

# Save the processed code back to a new file
with open(output_code_path, 'w') as file:
    file.write(processed_code)

print("Processed Solidity code has been saved without comments.")
