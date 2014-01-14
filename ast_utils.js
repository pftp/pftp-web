//used by ast_utils.py
//USAGE: node ast_utils.js <javascript_file>

if (process.argv.length != 3) {
  console.log('provide filename');
  process.exit(1);
}

useless_names = ['Program', 'AssignmentExpression', 'BlockStatement', 'EmptyStatement', 'VariableDeclarator'];
concepts = [];

reflect = require('reflect');
traverse = require('ast-traverse');
//burrito = require('burrito');
fs = require('fs');
fs.readFile(process.argv[2], 'utf8', function(err, data) {
  if (err)
    return console.log(err);
  //src = burrito(data, function (node) {
  //  console.log(node.node);
  //});
  var ast = reflect.parse(data);
  traverse(ast, {pre: function(node, parent, prop, idx) {
    if (useless_names.indexOf(node.type) == -1 && concepts.indexOf(node.type) == -1)
      concepts.push(node.type);
  }});

  for (var i = 0; i < concepts.length; i++) {
    console.log(concepts[i]);
  }
});
