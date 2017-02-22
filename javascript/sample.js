const fs = require('fs');
const path = require('path');
const parser = require('./wdl_parser.js');

if(process.argv.length < 3) {
   console.error('node sample.js <file.wdl>');
   return;
}

try {
    const wdlPath = process.argv[2];
    const wdl = fs.readFileSync(wdlPath).toString();
    const tokens = parser.lex(wdl);
    const ast = parser.parse(tokens).to_ast();

    console.log(parser.ast_string(ast, 2, true));
}
catch(ex) {
    console.error(ex.message);
}
