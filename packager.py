import ast
import os
import shutil

class Packager:
  def __init__(self, name, paths):
    self.name = name
    self.paths = paths
  
  def get_imports(self):
    imports = []
    for path in self.paths:
      with open(path) as fh:
         root = ast.parse(fh.read(), path)
    
      for node in ast.iter_child_nodes(root):
        if isinstance(node, ast.Import):
          module = []
        elif isinstance(node, ast.ImportFrom):  
          module = node.module.split('.')
        else:
          continue
        if module:
          if module[0] == 'includes':
            imports.append(module)

    #Recursively Merge Imports
    for i in imports:
      ri = Packager('', ['/'.join(i)+".py"]).get_imports()
      for recursiveImport in ri:
        if recursiveImport not in imports:
          imports.append(recursiveImport)
    return imports

  def package(self):
    for p in self.get_imports():
      path = 'packages/' + '/'.join(p) + ".py"
      directory = 'packages/' + '/'.join(p[:-1])
      if not os.path.exists(directory):
        os.makedirs(directory)
      shutil.copy('/'.join(p)+".py", path)
    for p in self.paths:
      splitPath = p.split('/')
      path = 'packages/' + '/'.join(splitPath)
      directory = 'packages/' + '/'.join(splitPath[:-1])
      if not os.path.exists(directory):
        os.makedirs(directory)
      shutil.copy(p, path)
    shutil.make_archive('packages/includes', 'zip', 'packages/', 'includes')
    os.rename('packages/includes.zip', f'packages/{self.name}.zip')
    shutil.rmtree('packages/includes')

  def zip(self):
    pass

  def __str__(self):
    return str(self.paths)+":\n"+'\n'.join([str('/'.join(imp)) for imp in self.get_imports()])

  def __repr(self):
    return str(self)