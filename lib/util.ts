function getCodeSnippetDetails(sourceCode: string, startLine: number, endLine: number): { startIndex: number, length: number } | null {
    // Split the source code into lines
    const lines = sourceCode.split('\n');

    // Check if the start and end lines are within the range of the source code lines
    if (startLine < 1 || endLine > lines.length || startLine > endLine) {
        console.error('Invalid start or end line numbers.');
        return null;
    }

    // Initialize the startIndex to -1 to denote that it hasn't been set yet
    let startIndex = -1;
    let length = 0;

    for (let i = 0; i < lines.length; i++) {
        if (i === startLine - 1) {
            // For the start line, calculate the startIndex (if it's not already set)
            // Trim leading whitespaces or tabs before calculating startIndex
            startIndex = length + (lines[i].length - lines[i].trimStart().length);
        }

        // If within the range from startLine to endLine, add the line length and newline character length
        // Add the length of the line plus one for the newline character
        if (i >= startLine - 1 && i <= endLine - 1) {
            length += lines[i].length + 1; // +1 for the newline character
        }

        // For all lines before the endLine, add the length of the line plus one for the newline character
        if (i < endLine - 1) {
            length += lines[i].length + 1; // +1 for the newline character
        } else if (i === endLine - 1) {
            // For the end line, just add the length of the line
            length += lines[i].length;
            break; // No need to process further lines
        }
    }

    return startIndex !== -1 ? { startIndex, length } : null;
}

// Usage example
const sourceCode = `pragma solidity ^0.4.13;

contract TestConditional {
    function conditionalSimple(uint a) public returns (uint) {
        return a > 10 ? 10 : 15;
    }

    function conditionalWithNested(uint a) public returns (uint) {
        return (a > 10 ? true : false)
            ? a > 15 ? 20 : a
            : a < 5 ? a : 0;
    }

    function conditionalWithComplexExpressions(uint a) public returns (uint) {
        return a % 2 == 0 ? this.sqrt(a) + 10 : a * 6 / 2;
    }

    function sqrt(uint x) public returns (uint y) {
        uint z = (x + 1) / 2;

        y = x;

        while (z < y) {
            y = z;

            z = (x / z + z) / 2;
        }
    }
}`;
const startLine = 4;
const endLine = 15;
const details = getCodeSnippetDetails(sourceCode, startLine, endLine);
if (details) {
    console.log('Start Index:', details.startIndex); // Index of the first non-whitespace character in the start line within the entire source code
    console.log('Length:', details.length); // Total length of the snippet from startLine to endLine
}
