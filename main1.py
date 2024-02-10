def find_enclosing_elements(solidity_code, start_line, end_line):
    # Normalize line endings and split the code into lines
    lines = solidity_code.replace('\r\n', '\n').split('\n')

    # Initialize variables to keep track of contracts and functions
    current_contract = None
    current_function = None
    enclosing_contract = None
    enclosing_function = None
    contract_start_line = float('-inf')
    function_start_line = float('-inf')
    function_end_line = float('inf')

    # Flags to detect if the range spans across multiple functions
    is_within_function = False
    multiple_functions = False

    # Iterate over the lines of the code
    for i, line in enumerate(lines):
        # Check for contract declaration
        if 'contract ' in line:
            # Set the current contract
            current_contract = line
            contract_start_line = i + 1

            # Reset function-related variables
            current_function = None
            function_start_line = float('inf')
            function_end_line = float('inf')
            is_within_function = False

        # Check for function or constructor declaration
        elif 'function ' in line or 'constructor' in line:
            current_function = line
            function_start_line = i + 1
            is_within_function = False

        # Check for the end of a function or constructor block
        elif current_function and '{' in line:
            # This is a simplified assumption that the '{' marks the end of the function signature
            function_end_line = i + 1

        # Check if the current line number is within the range of start_line and end_line
        if start_line <= i + 1 <= end_line:
            if current_contract and contract_start_line <= i + 1:
                enclosing_contract = current_contract
            if current_function and function_start_line <= i + 1 <= function_end_line:
                is_within_function = True
                enclosing_function = current_function
            elif is_within_function and (i + 1 > function_end_line or '}' in line):
                # If the range spans outside the current function, reset enclosing_function
                is_within_function = False
                multiple_functions = True
                enclosing_function = None

    # If the range spans multiple functions or is outside any function, reset enclosing_function to None
    if multiple_functions or not is_within_function:
        enclosing_function = None

    return enclosing_contract, enclosing_function


# Test the function with an example
solidity_code = """// SPDX-License-Identifier: MIT
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
}
"""

print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")

# Test Case 1: Inside the Car contract constructor
start_line = 10
end_line = 11

enclosing_contract, enclosing_function = find_enclosing_elements(
    solidity_code, start_line, end_line)
print(f'Test case 1: For start_line: {start_line} and end_line: {end_line}')
print(f'Enclosing contract: {enclosing_contract}')
print(f'Enclosing function: {enclosing_function}')
print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")

# Test Case 2: Inside the create function of the CarFactory contract
start_line = 16
end_line = 16

enclosing_contract, enclosing_function = find_enclosing_elements(
    solidity_code, start_line, end_line)
print(f'Test case 2: For start_line: {start_line} and end_line: {end_line}')
print(f'Enclosing contract: {enclosing_contract}')
print(f'Enclosing function: {enclosing_function}')
print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")

# Test Case 3: Inside the createAndSendEther function of the CarFactory contract
start_line = 20
end_line = 20

enclosing_contract, enclosing_function = find_enclosing_elements(
    solidity_code, start_line, end_line)
print(f'Test case 3: For start_line: {start_line} and end_line: {end_line}')
print(f'Enclosing contract: {enclosing_contract}')
print(f'Enclosing function: {enclosing_function}')
print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")

# Test Case 4: Inside the create2 function of the CarFactory contract
start_line = 24
end_line = 24

enclosing_contract, enclosing_function = find_enclosing_elements(
    solidity_code, start_line, end_line)
print(f'Test case 4: For start_line: {start_line} and end_line: {end_line}')
print(f'Enclosing contract: {enclosing_contract}')
print(f'Enclosing function: {enclosing_function}')
print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")

# Test Case 5: Inside the create2AndSendEther function of the CarFactory contract
start_line = 29
end_line = 29

enclosing_contract, enclosing_function = find_enclosing_elements(
    solidity_code, start_line, end_line)
print(f'Test case 5: For start_line: {start_line} and end_line: {end_line}')
print(f'Enclosing contract: {enclosing_contract}')
print(f'Enclosing function: {enclosing_function}')
print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")

# Test Case 6: Inside the getCar function of the CarFactory contract
start_line = 34
end_line = 34

enclosing_contract, enclosing_function = find_enclosing_elements(
    solidity_code, start_line, end_line)
print(f'Test case 6: For start_line: {start_line} and end_line: {end_line}')
print(f'Enclosing contract: {enclosing_contract}')
print(f'Enclosing function: {enclosing_function}')
print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")

# Test Case 7: Inside the Car contract but outside any function or constructor
start_line = 5
end_line = 5

enclosing_contract, enclosing_function = find_enclosing_elements(
    solidity_code, start_line, end_line)
print(f'Test case 7: For start_line: {start_line} and end_line: {end_line}')
print(f'Enclosing contract: {enclosing_contract}')
print(f'Enclosing function: {enclosing_function}')
print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")

# Test Case 8: Inside the CarFactory contract but outside any function
start_line = 15
end_line = 15

enclosing_contract, enclosing_function = find_enclosing_elements(
    solidity_code, start_line, end_line)
print(f'Test case 8: For start_line: {start_line} and end_line: {end_line}')
print(f'Enclosing contract: {enclosing_contract}')
print(f'Enclosing function: {enclosing_function}')
print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")

# Test Case 9: Spanning the entire Car contract, including the constructor
start_line = 4
end_line = 13

enclosing_contract, enclosing_function = find_enclosing_elements(
    solidity_code, start_line, end_line)
print(f'Test Case 9: For start_line: {start_line} and end_line: {end_line}')
print(f'Enclosing contract: {enclosing_contract}')
print(f'Enclosing function: {enclosing_function}')
print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")

# Test Case 10: Spanning the create function in the CarFactory contract
start_line = 16
end_line = 18

enclosing_contract, enclosing_function = find_enclosing_elements(
    solidity_code, start_line, end_line)
print(f'Test Case 10: For start_line: {start_line} and end_line: {end_line}')
print(f'Enclosing contract: {enclosing_contract}')
print(f'Enclosing function: {enclosing_function}')
print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")

# Test Case 11: Spanning from start of createAndSendEther to end of create2 in the CarFactory contract
start_line = 20
end_line = 26

enclosing_contract, enclosing_function = find_enclosing_elements(
    solidity_code, start_line, end_line)
print(f'Test Case 11: For start_line: {start_line} and end_line: {end_line}')
print(f'Enclosing contract: {enclosing_contract}')
print(f'Enclosing function: {enclosing_function}')
print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")

# Test Case 12: Spanning multiple functions, create2AndSendEther and getCar, in the CarFactory contract
start_line = 29
end_line = 38

enclosing_contract, enclosing_function = find_enclosing_elements(
    solidity_code, start_line, end_line)
print(f'Test Case 12: For start_line: {start_line} and end_line: {end_line}')
print(f'Enclosing contract: {enclosing_contract}')
print(f'Enclosing function: {enclosing_function}')
print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")

# Test Case 13: Spanning the entire CarFactory contract
start_line = 15
end_line = 40

enclosing_contract, enclosing_function = find_enclosing_elements(
    solidity_code, start_line, end_line)
print(f'Test Case 13: For start_line: {start_line} and end_line: {end_line}')
print(f'Enclosing contract: {enclosing_contract}')
print(f'Enclosing function: {enclosing_function}')
print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
