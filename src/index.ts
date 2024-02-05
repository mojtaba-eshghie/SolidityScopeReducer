import { CompileFailedError, CompileResult, compileSol } from "solc-typed-ast";


let result: CompileResult;

try {
    result = await compileSol("contracts/multiSigWallet.sol", "auto", []);
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

console.log(result);