import ast
import meta
import astpp

code = open('sample_code.py', 'r').read()
tree = ast.parse(code)

#Get source
source = meta.dump_python_source(tree)

#Get formatted AST repr
formatted_ast = astpp.dump(tree, include_attributes=True)

class FuncLister(ast.NodeVisitor):
  def visit_FunctionDef(self, node):
    print node.name
    self.generic_visit(node)

print 'Functions:'
FuncLister().visit(tree)
