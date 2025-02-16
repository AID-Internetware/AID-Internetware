from machinery.classes import ClassManager,ClassNode
from machinery.scopes import ScopeManager,ScopeItem
from machinery.definitions import DefinitionManager,Definition


class TypeInference:

    def __init__(self, class_manager: ClassManager, scope_manager: ScopeManager, definition_manager: DefinitionManager) -> None:

        #dict(ns, ClassNode)
        self._all_classes = class_manager.get_classes() 
        #dict(ns, ScopeItem)
        self._all_scopes = scope_manager.get_scopes()
        #dict(ns, Definition)
        self._all_definitions = definition_manager.get_defs()

        self._called_methods = dict()

        self._attribute_matching_to_class = dict()

        self._methods = dict()
        self._attributes = dict()
        self._methods_with_no_path = dict()
        self._attributes_with_no_path = dict()
    

    def get_all_methods_and_attributes(self):
            
        methods_and_attributes = dict()
        methods = dict()
        attributes = dict()
        
        for class_key, classNode in self._all_classes.items():
            for scope_key, scopeItem in self._all_scopes.items():
                if class_key == scope_key:
                    temp = set()
                    defs: dict = scopeItem.defs
                    #defi: Definition
                    for name, defi in defs.items():
                        temp.add(defi.fullns)                    
                    methods_and_attributes[class_key] = temp
                elif class_key in scope_key and class_key != scope_key and '<' not in scope_key and class_key.count('.') + 1 == scope_key.count('.'): 
                    if class_key not in methods:
                        methods[class_key] = set()
                        methods[class_key].add(scope_key)
                    else:
                        methods[class_key].add(scope_key)

        for class_name,set1 in methods_and_attributes.items():
            if class_name in methods:
                set2 = methods[class_name]
                set3 = set1 - set2
                attributes[class_name] = set3

        self._methods = methods
        self._attributes = attributes

        for key,sets in methods.items():
            if '\\' in key:
                temp = set()
                for v in sets:
                    temp.add(v.split('.')[-1])
                if temp:
                    self._methods_with_no_path[key] = temp
        
        for key,sets in attributes.items():
            if '\\' in key:
                temp = set()
                for v in sets:
                    temp.add(v.split('.')[-1])
                if temp:
                    self._attributes_with_no_path[key] = temp


    def collect_called_methods(self):
        
        called_methods = dict()
        for class_key, attributes_set in self._attributes.items():
            for attribute in attributes_set:
                attribute_no_path = attribute.split("\\")[-1]
                for defi_key, Definition in self._all_definitions.items():
                    values_set = Definition.points_to['name'].values
                    for value in values_set:
                        if attribute_no_path in value and attribute != value:
                            called_method = value.split(attribute_no_path + '.')[-1].split(".")[0]
                            if attribute not in called_methods:
                                called_methods[attribute] = set()
                                called_methods[attribute].add(called_method)
                            else:
                                called_methods[attribute].add(called_method)

        self._called_methods = called_methods


    def match(self):

        attribute_matching_to_class = dict()

        for attribute_name, called_methods in self._called_methods.items():
            for class_name, methods in self._methods.items():
                all_substrings = all(any(substring == s2.split('.')[-1] for s2 in methods) for substring in called_methods)
                if all_substrings:
                    if attribute_name not in attribute_matching_to_class:
                        attribute_matching_to_class[attribute_name] = set()
                        attribute_matching_to_class[attribute_name].add(class_name)
                    else:
                        attribute_matching_to_class[attribute_name].add(class_name)

        self._attribute_matching_to_class = attribute_matching_to_class


    def generate(self):

        self.get_all_methods_and_attributes()
        self.collect_called_methods()
        self.match()
        
       


