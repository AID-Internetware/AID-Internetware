from machinery.classes import ClassManager,ClassNode
from machinery.scopes import ScopeManager,ScopeItem
from machinery.definitions import DefinitionManager,Definition


class ParameterExtraction:

    def __init__(self, class_manager: ClassManager, scope_manager: ScopeManager, definition_manager: DefinitionManager) -> None:

        #dict(ns, ClassNode)
        self._all_classes = class_manager.get_classes() 
        #dict(ns, ScopeItem)
        self._all_scopes = scope_manager.get_scopes()
        #dict(ns, Definition)
        self._all_definitions = definition_manager.get_defs()

        #(parameter, )
        self._parameters = dict()


    def get_parameter(self):
        for defi_key, Definition in self._all_definitions.items():
            if Definition.def_type == 'FUNCTIONDEF':
                method = Definition.fullns
                parameters_dict = Definition.points_to['name'].args
                for k, v in parameters_dict.items():
                    self._parameters[list(v)[0]] = method 
