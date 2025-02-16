import ast
import os


#directory_path = "C:/Users/40382/Desktop/NewPyCG/SDK_dataset/pyfritzhome"
directory_path = "C:/Users/40382/Desktop/NewPyCG/SDK_dataset/pymystrom"



class PropertyVisitor(ast.NodeVisitor):
    def __init__(self):
        self.property_methods = []

    def visit_FunctionDef(self, node):
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name) and decorator.id == "property":
                self.property_methods.append(node.name)
        self.generic_visit(node)


def find_property_methods(directory):
    property_methods = {}
    methods_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        tree = ast.parse(f.read(), file_path)
                        visitor = PropertyVisitor()
                        visitor.visit(tree)
                        if visitor.property_methods:
                            property_methods[file] = visitor.property_methods
                            methods_list.extend(visitor.property_methods)
                    except SyntaxError as e:
                        print(f"SyntaxError in {file_path}: {e}")
    return property_methods, methods_list




if __name__ == "__main__":


    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                property_methods = {}
                methods_list = []
                new_methods_list = set()
                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                                               
                        tree = ast.parse(f.read(), file_path)
                        visitor = PropertyVisitor()
                        visitor.visit(tree)
                        if visitor.property_methods:
                            property_methods[file] = visitor.property_methods
                            methods_list.extend(visitor.property_methods)
                        
                        new_methods_list = set('.' + item for item in methods_list)
                        print(new_methods_list)
                    except SyntaxError as e:
                        print(f"SyntaxError in {file_path}: {e}")
                with open(file_path, "r", encoding="utf-8") as f2:  
                    try:
                        filedata = f2.read()
                        for function in new_methods_list:
                            if function in filedata:
                                filedata = filedata.replace(function + " ", function + "() ")

                                filedata = filedata.replace(function + "() =", function + " =")

                                filedata = filedata.replace(function + "}", function + "()}")
                                filedata = filedata.replace(function + "()} =", function + "} =")

                                filedata = filedata.replace(function + "]", function + "()]")
                                filedata = filedata.replace(function + "()] =", function + "] =")
                                
                                filedata = filedata.replace(function + ")", function + "())")
                                filedata = filedata.replace(function + "()) =", function + ") =")

                                filedata = filedata.replace(function + ",", function + "(),")
                                filedata = filedata.replace(function + "(), =", function + ", =")

                                filedata = filedata.replace(function + ".", function + "().")
                                filedata = filedata.replace(function + "(). =", function + ". =")

                                filedata = filedata.replace(function + ":", function + "():")
                                filedata = filedata.replace(function + "(): =", function + ": =")

                                filedata = filedata.replace(function + ";", function + "();")
                                filedata = filedata.replace(function + "(); =", function + "; =")

                                filedata = filedata.replace(function + "\n", function + "()\n")
                                filedata = filedata.replace(function + "()\n =", function + "\n =")
                                with open(file_path, 'w') as file2:
                                    file2.write(filedata)                            
                    except SyntaxError as e:
                        print(f"SyntaxError in {file_path}: {e}")




