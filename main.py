def find_enclosing_elements(solidity_code, start_line, end_line):
    # Normalize line endings and split the code into lines
    lines = solidity_code.replace('\r\n', '\n').split('\n')

    # Initialize variables to keep track of contracts and functions
    current_contract = None
    current_function = None
    enclosing_contract = None  # Initialize enclosing_contract
    enclosing_function = None  # Initialize enclosing_function
    contract_start_line = float('inf')
    function_start_line = float('inf')
    # Track the end line of the current function
    function_end_line = float('inf')

    # Iterate over the lines of the code
    for i, line in enumerate(lines):
        # Check if the line is a contract or function declaration
        if 'contract ' in line:
            if current_contract and start_line >= contract_start_line:
                # If within the current contract scope, assign it as enclosing
                enclosing_contract = current_contract
            current_contract = line
            contract_start_line = i + 1
            # When a new contract is found, reset the function info
            current_function = None
            function_start_line = float('inf')
            function_end_line = float('inf')
        elif 'function ' in line or 'constructor' in line:
            # Close the previous function scope when a new function starts
            if current_function and start_line >= function_start_line and end_line <= function_end_line:
                enclosing_function = current_function
            current_function = line
            function_start_line = i + 1
            # Reset end line for the new function
            function_end_line = float('inf')
        elif current_function and '{' in line:
            # This simplistic approach assumes functions are well-structured and '{' appears only once
            # Tentatively mark the end of the function at the '{'
            function_end_line = i + 1

        # Check if the current line number is within the range of start_line and end_line
        if start_line <= i + 1 <= end_line:
            # Check if we've passed the start of a new contract or function
            if current_contract and contract_start_line <= i + 1:
                enclosing_contract = current_contract
            if current_function and function_start_line <= i + 1 and function_end_line >= i + 1:
                enclosing_function = current_function
            else:
                # If the range spans more than the bounds of the current function, reset enclosing_function
                enclosing_function = None

    # Final check for the last function in the file
    if current_function and start_line >= function_start_line and end_line <= function_end_line:
        enclosing_function = current_function

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
