import json
import solcx
import solcast
import copy

# Ensure solcx is installed and set to the correct Solidity compiler version
solcx.install_solc('0.5.17')  # Use the appropriate version for your contract
solcx.use_solc('0.5.17')
# Compile Solidity contracts to standard JSON output format


def compile_solidity_contract(file_path):
    with open(file_path, 'r') as file:
        source_code = file.read()

    # Prepare input JSON for compilation with AST output
    input_json = {
        'language': 'Solidity',
        'sources': {file_path: {'content': source_code}},
        'settings': {
            'outputSelection': {
                '*': {
                    '*': ['metadata', 'evm.bytecode', 'evm.bytecode.sourceMap', 'abi'],
                    '': ['ast']  # Requesting AST output here
                }
            }
        }
    }

    # Compile and return output JSON
    output_json = solcx.compile_standard(input_json, allow_paths=".")
    return output_json

# Parse the AST from compiled output and print


def print_contract_ast(compiled_sol):
    nodes = solcast.from_standard_output(compiled_sol)
    for node in nodes:
        print(node)
        # Example to explore further: print the names of contracts in a SourceUnit
        for child in node['nodes']:
            if child['nodeType'] == 'ContractDefinition':
                print(f"Contract Name: {child['name']}")


def get_enclosing_function_and_contract(output_json, solidity_filename, start_line, end_line):
    function = None
    contract = None

    nodes = solcast.from_standard_output(output_json)
    root_node = solcast.from_ast(output_json["sources"]["sample2.sol"]["ast"])

    source_code = open(solidity_filename, 'r').read()
    source_code_lines = source_code.split('\n')
    start_index = 0
    for i in range(0, start_line):
        if i < start_line - 1:
            start_index += len(source_code_lines[i])
        else:
            start_index += len(source_code_lines[i]) - \
                len(source_code_lines[i].lstrip(' '))

    end_index = start_index
    for j in range(start_line-1, end_line):
        end_index += len(source_code_lines[j])

    result = root_node.children(required_offset=(start_index, end_index))
    '''
    print(result[0])
    print(result[0].offset)
    print(result[0].nodeType)
    print('----')
    print(result[1])
    print(result[1].offset)
    print(result[1].nodeType)
    print(result[1].name)
    '''

    for node in result:
        if node.nodeType == 'ContractDefinition':
            contract = {
                "offset": node.offset,
                "name": node.name
            }
        elif node.nodeType == 'FunctionDefinition':
            function = {
                "offset": node.offset,
                "name": node.name
            }

    return {
        "contract": contract,
        "function": function
    }


result = get_enclosing_function_and_contract(
    compile_solidity_contract('sample2.sol'), 'sample2.sol', 104, 109)

print(result)
'''
# Main execution
if __name__ == "__main__":
    file_path = 'sample2.sol'  # Update with your contract's file name
    output_json = compile_solidity_contract(file_path)
    # print(output_json)
    nodes = solcast.from_standard_output(output_json)
    root_node = solcast.from_ast(output_json["sources"]["sample2.sol"]["ast"])
    # print(root_node.offset)
    print(root_node.children(required_offset=(87, 135)))
    print(root_node.children(required_offset=(256, 285)))

    print(root_node.children()[2].offset)

    # print(nodes)
    # print_contract_ast(compiled_sol)
'''
