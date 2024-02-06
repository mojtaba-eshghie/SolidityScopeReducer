def analyze_smart_contract(source_code):
    lines = source_code.split('\n')
    definitions = []
    current_definition = None
    in_contract = False
    brace_stack = []  # Use a stack to track opening and closing braces

    for i, line in enumerate(lines):
        line_stripped = line.strip()
        # Check for contract definition
        if line_stripped.startswith('contract '):
            if current_definition and brace_stack:  # End the previous definition if braces are balanced
                current_definition['end_line'] = i
                definitions.append(current_definition)
            current_definition = {
                'type': 'contract',
                'start_line': i + 1  # +1 to convert from 0-based to 1-based indexing
            }
            in_contract = True
            brace_stack = []  # Reset brace stack for a new contract
        # Check for function definition within a contract
        elif in_contract and line_stripped.startswith('function '):
            if current_definition and current_definition['type'] == 'function' and not brace_stack:
                # End the previous function definition if braces are balanced (no nested structures)
                current_definition['end_line'] = i
                definitions.append(current_definition)
            current_definition = {
                'type': 'function',
                'start_line': i + 1
            }

        # Process opening brace
        if '{' in line:
            brace_stack.append(i + 1)  # Store line number of the opening brace
        # Process closing brace
        if '}' in line and brace_stack:
            brace_stack.pop()
            if not brace_stack:  # If the stack is empty, we've closed a function or contract block
                if current_definition:
                    current_definition['end_line'] = i + 1
                    definitions.append(current_definition)
                    current_definition = None
                in_contract = False  # We might have ended a contract block, reset the flag

    # Final check if the file ends with an open definition
    if current_definition:
        current_definition['end_line'] = len(lines)
        definitions.append(current_definition)

    return definitions


source_code = '''// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

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

contract CarFactory {
    Car[] public cars;

    function create(address _owner, string memory _model) public {
        Car car = new Car(_owner, _model);
        cars.push(car);
    }

    function createAndSendEther(address _owner, string memory _model) public payable {
        Car car = (new Car){value: msg.value}(_owner, _model);
        cars.push(car);
    }

    function create2(address _owner, string memory _model, bytes32 _salt) public {
        Car car = (new Car){salt: _salt}(_owner, _model);
        cars.push(car);
    }

    function create2AndSendEther(
        address _owner,
        string memory _model,
        bytes32 _salt
    ) public payable {
        Car car = (new Car){value: msg.value, salt: _salt}(_owner, _model);
        cars.push(car);
    }

    function getCar(
        uint _index
    )
        public
        view
        returns (address owner, string memory model, address carAddr, uint balance)
    {
        Car car = cars[_index];

        return (car.owner(), car.model(), car.carAddr(), address(car).balance);
    }
}'''

definitions = analyze_smart_contract(source_code)
print(definitions)
