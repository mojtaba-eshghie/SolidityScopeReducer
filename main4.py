def analyze_smart_contract(source_code):
    lines = source_code.split('\n')
    definitions = []
    current_definition = None

    for i, line in enumerate(lines):
        # Check for contract or function definition
        if 'contract' in line or 'def' in line:
            # If there's a current definition, mark its end line
            if current_definition:
                current_definition['end_line'] = i
                definitions.append(current_definition)

            # Start tracking a new definition
            current_definition = {
                'type': 'contract' if 'contract' in line else 'function',
                'start_line': i + 1  # +1 to convert from 0-based to 1-based indexing
            }

    # If the file ends with a definition, mark its end line
    if current_definition:
        current_definition['end_line'] = len(lines)
        definitions.append(current_definition)

    return definitions


# Test with a sample smart contract source code
source_code = """contract MyContract {
    function doSomething() {
        // implementation
    }
    
    function doSomethingElse() {
        // implementation
    }
}

contract Car {
    address public owner;
    string public model;
    address public carAddr;

    constructor(address _owner, string memory _model) payable {
        owner = _owner;
        model = _model;
        carAddr = address(this);
    }
}
"""
definitions = analyze_smart_contract(source_code)
for definition in definitions:
    print(
        f"{definition['type']} starts at line {definition['start_line']} and ends at line {definition['end_line']}")

print(definitions)
