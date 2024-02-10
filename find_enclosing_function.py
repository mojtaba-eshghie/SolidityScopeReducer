def find_enclosing_function(file_path, chunk_start, chunk_end):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    elements = []  # This will include both functions and constructors

    # Identify where each function and constructor starts and ends
    for i, line in enumerate(lines):
        stripped_line = line.strip()
        if stripped_line.startswith('function ') or stripped_line.startswith('constructor '):
            elements.append(
                {'start': i, 'type': 'function' if 'function ' in stripped_line else 'constructor'})

    # Mark the end of each function/constructor by the start of the next one
    for i in range(len(elements) - 1):
        elements[i]['end'] = elements[i + 1]['start']
    elements[-1]['end'] = len(lines)

    # Find the function/constructor that encloses the specified chunk of code
    for element in elements:
        if element['start'] <= chunk_start and element['end'] >= chunk_end:
            return ''.join(lines[element['start']:element['end']])

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
            result = find_enclosing_function(
                file_path, test['start_line'], test['end_line'])
            if result is None:
                print(
                    f"Result for test #{test['test_id']} ({test['start_line']}, {test['end_line']}) : {result}")
            else:
                # function_body = '\n'.join(result.split('\n')[:-3])
                function_body = result
                print(
                    f"Result for test #{test['test_id']} ({test['start_line']}, {test['end_line']}) : {function_body}")
        except Exception as e:
            print(f"Error: {e}")


# Run the tests
run_tests()
