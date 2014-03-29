# USAGE: python ast_utils.py <{python, javascript}_file>
# Prints a list of all relevant concepts from file by traversing its ast

import sys
import ast
import os
import tempfile
import subprocess

def node_type(node):
  return type(node).__name__.lower()

class ConceptVisitor(ast.NodeVisitor):
  def __init__(self):
    self.useless_names = ['module', 'interactive', 'expressoin', 'suite', 'expr', 'load', 'store', 'del', 'augload', 'augstore', 'param', 'comprehension', 'excepthandler', 'arguments', 'alias']
    self.user_defs = []
    self.modules = {}
    self.concepts = []

  def generic_visit(self, node):
    node_name = node_type(node)
    if node_name not in self.useless_names and node_name not in self.concepts:
      self.concepts.append(node_name)
    for child in ast.iter_child_nodes(node):
      self.visit(child)

  def visit_FunctionDef(self, node):
    if node.name not in self.user_defs:
      self.user_defs.append(node.name)
    self.generic_visit(node)

  def visit_Import(self, node):
    for alias_node in node.names:
      if alias_node.name not in self.modules and alias_node.asname not in self.modules:
        modname = 'mod_' + alias_node.name
        if modname not in self.concepts:
          self.concepts.append(modname)
        if alias_node.asname == None:
          self.modules[alias_node.name] = alias_node.name
        else:
          self.modules[alias_node.asname] = alias_node.name
          if 'importas' not in self.concepts:
            self.concepts.append('importas')
    self.generic_visit(node)

  def visit_ImportFrom(self, node):
    modname = 'mod_' + node.module
    if modname not in self.concepts:
      self.concepts.append(modname)
    self.generic_visit(node)

class FuncVisitor(ast.NodeVisitor):
  def __init__(self, user_defs, modules):
    self.user_defs = user_defs
    self.modules = modules
    self.concepts = []

  def visit_Call(self, node):
    ntype = node_type(node.func)
    if ntype == 'name':
      func_name = 'func_' + node.func.id
      if node.func.id not in self.user_defs and func_name not in self.concepts:
        self.concepts.append(func_name)
    elif ntype == 'attribute':
      attr_value = node.func.value
      if node_type(attr_value) == 'name' and attr_value.id in self.modules:
        func_name = 'modfunc_' + self.modules[attr_value.id] + '_' + node.func.attr
        if func_name not in self.concepts:
          self.concepts.append(func_name)
      else:
        func_name = 'func_' + node.func.attr
        if node.func.attr not in self.user_defs and func_name not in self.concepts:
          self.concepts.append(func_name)

def get_concepts(src_str, language_id):
  #TODO detect language automatically
  if language_id == 1:
    src_ast = ast.parse(src_str)
    cv = ConceptVisitor()
    cv.visit(src_ast)
    fv = FuncVisitor(cv.user_defs, cv.modules)
    fv.visit(src_ast)
    return cv.concepts + fv.concepts
  else:
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.write(src_str)
    tmp.close()
    process = subprocess.Popen(['node', 'ast_utils.js', tmp.name], stdout=subprocess.PIPE)
    out, err = process.communicate()
    os.unlink(tmp.name)
    return filter(lambda x: len(x) > 0, out.split('\n'))

if __name__ == '__main__':
  f = open(sys.argv[1])
  x = f.read()
  f.close()
  languages = {'py': 1, 'js': 1}
  print get_concepts(x, 1)
