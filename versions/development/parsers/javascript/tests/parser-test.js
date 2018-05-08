const assert = require('assert');
const fs = require('fs');
const path = require('path');
const parser = require('../wdl_parser.js');

function getDirectories (srcpath) {
  return fs.readdirSync(srcpath)
    .filter(file => fs.statSync(path.join(srcpath, file)).isDirectory())
    .map(directory => path.join(srcpath, directory));
}

function removeLinebreaks(input) {
    return input.replace(/[\r\n]/g, '');
}

describe('JS-WDL Parser', function () {
    const cases = getDirectories(path.resolve('./cases'));
    
    cases.forEach(function(casePath) {
        it('should correctly generate ast for ' + casePath, function () {
            
            //Read wdl test case to generate ast
            const wdl = fs.readFileSync(path.resolve(casePath, "wdl")).toString();

            //Parse wdl into ast
            const tokens = parser.lex(wdl);
            const astObj = parser.parse(tokens).to_ast();
            const astParsed = parser.ast_string(astObj, 2, true)

            //If no 'original' ast found in a test case directory - regenerate it
            const astTestCasePath = path.resolve(casePath, "ast");
            if(!fs.existsSync(astTestCasePath)) {
                fs.writeFileSync(astTestCasePath, astParsed);
            }
            const astTestCase = fs.readFileSync(astTestCasePath).toString();

            //Line breaks are removed not to face Linux/Windows and Git settings line endings issues
            assert(removeLinebreaks(astParsed) === removeLinebreaks(astTestCase), 'ASTs are not equal');
        });
    });
});
