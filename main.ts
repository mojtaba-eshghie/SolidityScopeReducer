import { CompileFailedError, CompileResult, compileSol, compileJson, ASTReader, ASTWriter, DefaultASTWriterMapping, LatestCompilerVersion, PrettyFormatter } from "solc-typed-ast";

let result: CompileResult;

const formatter = new PrettyFormatter(4, 0);

const filePath = "contracts/multiSigWallet.sol";

try {
    result = await compileSol(filePath, "auto");
} catch (e) {
    if (e instanceof CompileFailedError) {
        console.error("Compile errors encountered:");

        for (const failure of e.failures) {
            console.error(`Solc ${failure.compilerVersion}:`);

            for (const error of failure.errors) {
                console.error(error);
            }
        }
    } else {
        console.error(e.message);
    }
}


// Extract ASTs from the compilation result

const reader = new ASTReader();
const asts = reader.read(result.data);
console.log("ASTs are: ");
console.log(asts[0].getChildren());

/*
console.log("Used compiler version: " + result.compilerVersion);

// getChildren() returns an array of AST nodes
const children = asts[0].getChildren();


// create a new AST writer
const writer = new ASTWriter(
    DefaultASTWriterMapping,
    formatter,
    result.compilerVersion ? result.compilerVersion : LatestCompilerVersion
);

// read source code file 

const fs = require('fs');
const source = fs.readFileSync(filePath, 'utf8').toString();


// iterate over all children to find require statements

var id = 0;
for (const child of children) {
    if (child.name === "require") {
        console.log("Found require statement at " + child.print());


        var req_position = child.getParents()[0].src.split(":");

        if (req_position) {
            var slice = source.substr(parseInt(req_position[0]), parseInt(req_position[1])+1);
            var src_copy = source;
            var new_src = src_copy.replace(slice, "require(<condition>, <message>);");

            fs.writeFileSync('out/HelloWorld' + id + '.sol', new_src, 'utf8');
        } 
        id++;
    }
}
*/