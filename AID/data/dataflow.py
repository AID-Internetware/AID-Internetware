from machinery.classes import ClassManager,ClassNode
from machinery.scopes import ScopeManager,ScopeItem
from machinery.definitions import DefinitionManager,Definition


class Dataflow:
    
    def __init__(self, class_manager: ClassManager, scope_manager: ScopeManager, definition_manager: DefinitionManager) -> None:

        #dict(ns, ClassNode)
        self._all_classes = class_manager.get_classes() 
        #dict(ns, ScopeItem)
        self._all_scopes = scope_manager.get_scopes()
        #dict(ns, Definition)
        self._all_definitions = definition_manager.get_defs()


        self._methods = set()
        #self._attributes = dict()

        #ns, set(pointer)
        self._return_information = dict()

        self._class_variable_information = dict()
        self._function_parameter_variable_information = dict()

        self._assign_information = dict()

    def get_all_methods(self):
        
        for defi_key, Definition in self._all_definitions.items():
            if Definition.def_type == 'FUNCTIONDEF':
                self._methods.add(Definition.fullns)

    def get_assign(self):

        for class_key, classNode in self._all_classes.items():
            for scope_key, scopeItem in self._all_scopes.items():
                if class_key == scope_key:
                    for key, Definition in scopeItem.defs.items():
                        if len(Definition.points_to['name'].values) != 0:
                            self._class_variable_information[Definition.fullns] = Definition.points_to['name'].values
                elif class_key in scope_key and class_key != scope_key and '<' not in scope_key:
                    for key, Definition in scopeItem.defs.items():
                        if len(Definition.points_to['name'].values) != 0:
                            self._function_parameter_variable_information[Definition.fullns] = Definition.points_to['name'].values

        for key, sets in self._class_variable_information.items():
            for value in sets:
                if value not in self._assign_information:
                    self._assign_information[value.split(".<RETURN>")[0]] = set()
                self._assign_information[value.split(".<RETURN>")[0]].add(key.split(".<RETURN>")[0])

        for key, sets in self._function_parameter_variable_information.items():
            for value in sets:
                if value not in self._assign_information:
                    self._assign_information[value.split(".<RETURN>")[0]] = set()
                self._assign_information[value.split(".<RETURN>")[0]].add(key.split(".<RETURN>")[0])

    def get_parameter(self):
        pass

    def get_return(self):
        
        temp_dict = dict()

        for defi_key, Definition in self._all_definitions.items():
            if "<RETURN>" in defi_key and len(Definition.points_to['name'].values) != 0:
                temp_dict[defi_key] = Definition.points_to['name'].values

        for key, sets in temp_dict.items():
            for value in sets:
                if value not in self._return_information:
                    self._return_information[value.split(".<RETURN>")[0]] = set()
                self._return_information[value.split(".<RETURN>")[0]].add(key.split(".<RETURN>")[0])





