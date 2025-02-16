import os

import utils
from machinery.callgraph import CallGraph
from machinery.classes import ClassManager
from machinery.definitions import DefinitionManager
from machinery.imports import ImportManager
from machinery.key_err import KeyErrors
from machinery.modules import ModuleManager
from machinery.scopes import ScopeManager
from processing.cgprocessor import CallGraphProcessor
from processing.keyerrprocessor import KeyErrProcessor
from processing.postprocessor import PostProcessor
from processing.preprocessor import PreProcessor

from inference.type import TypeInference
from data.dataflow import Dataflow
from data.parameter import ParameterExtraction


class CallGraphGenerator(object):
    def __init__(self, entry_points, package, max_iter, operation):
        self.entry_points = entry_points
        self.package = package
        self.state = None
        self.max_iter = 10
        self.operation = operation
        self.setUp()

    def setUp(self):
        self.import_manager = ImportManager()
        self.scope_manager = ScopeManager()
        self.def_manager = DefinitionManager()
        self.class_manager = ClassManager()
        self.module_manager = ModuleManager()
        self.cg = CallGraph()
        self.key_errs = KeyErrors()

    def extract_state(self):
        state = {}
        state["defs"] = {}
        for key, defi in self.def_manager.get_defs().items():
            state["defs"][key] = {
                "names": defi.get_name_pointer().get().copy(),
                "lit": defi.get_lit_pointer().get().copy(),
            }

        state["scopes"] = {}
        for key, scope in self.scope_manager.get_scopes().items():
            state["scopes"][key] = set(
                [x.get_ns() for (_, x) in scope.get_defs().items()]
            )

        state["classes"] = {}
        for key, ch in self.class_manager.get_classes().items():
            state["classes"][key] = ch.get_mro().copy()
        return state

    def reset_counters(self):
        for key, scope in self.scope_manager.get_scopes().items():
            scope.reset_counters()

    def has_converged(self):
        if not self.state:
            return False

        curr_state = self.extract_state()
        
        # check defs
        for key, defi in curr_state["defs"].items():
            if key not in self.state["defs"]:
                return False
            if defi["names"] != self.state["defs"][key]["names"]:
                return False
            if defi["lit"] != self.state["defs"][key]["lit"]:
                return False

        # check scopes
        for key, scope in curr_state["scopes"].items():
            if key not in self.state["scopes"]:
                return False
            if scope != self.state["scopes"][key]:
                return False

        # check classes
        for key, ch in curr_state["classes"].items():
            if key not in self.state["classes"]:
                return False
            if ch != self.state["classes"][key]:
                return False

        return True

    def remove_import_hooks(self):
        self.import_manager.remove_hooks()

    def tearDown(self):
        self.remove_import_hooks()

    def _get_mod_name(self, entry, pkg):
        # We do this because we want __init__ modules to
        # only contain the parent module
        # since pycg can't differentiate between functions
        # coming from __init__ files.

        input_mod = utils.to_mod_name(os.path.relpath(entry, pkg))

        return input_mod

    def do_pass(self, cls, install_hooks=False, *args, **kwargs):

        modules_analyzed = set()

        for entry_point in self.entry_points:
            input_pkg = self.package
            input_mod = self._get_mod_name(entry_point, input_pkg)
            input_file = os.path.abspath(entry_point)

            if not input_mod:
                continue

            if not input_pkg:
                input_pkg = os.path.dirname(input_file)

            if input_mod not in modules_analyzed:
                if install_hooks:
                    self.import_manager.set_pkg(input_pkg)
                    self.import_manager.install_hooks()

                processor = cls(
                    input_file,
                    input_mod,
                    modules_analyzed=modules_analyzed,
                    *args,
                    **kwargs,
                )
                processor.analyze()

                modules_analyzed = modules_analyzed.union(
                    processor.get_modules_analyzed()
                )

                if install_hooks:
                    self.remove_import_hooks()

    def do_pass_attribute_matching_to_class(self, cls, install_hooks=False, *args, **kwargs):

        modules_analyzed = set()

        for entry_point in self.entry_points:
            input_pkg = self.package
            input_mod = self._get_mod_name(entry_point, input_pkg)
            input_file = os.path.abspath(entry_point)

            if not input_mod:
                continue

            if not input_pkg:
                input_pkg = os.path.dirname(input_file)

            if input_mod not in modules_analyzed:
                if install_hooks:
                    self.import_manager.set_pkg(input_pkg)
                    self.import_manager.install_hooks()

                processor = cls(
                    input_file,
                    input_mod,
                    modules_analyzed=modules_analyzed,
                    *args,
                    **kwargs,
                )
                processor.analyze()

                modules_analyzed = modules_analyzed.union(
                    processor.get_modules_analyzed()
                )

                if install_hooks:
                    self.remove_import_hooks()

    def analyze(self):
        self.do_pass(
            PreProcessor,
            True,
            self.import_manager,
            self.scope_manager,
            self.def_manager,
            self.class_manager,
            self.module_manager,
        )
        self.def_manager.complete_definitions()


        '''print("预处理完成")
        print("____________________________________")
        print("____________________________________")
        print("____________________________________")'''
        #预处理结束后提取属性
        parameterExtraction = ParameterExtraction(self.class_manager, self.scope_manager, self.def_manager)
        parameterExtraction.get_parameter()


        iter_cnt = 0
        while (self.max_iter < 0 or iter_cnt < self.max_iter) and (
            not self.has_converged()
        ):
            self.state = self.extract_state()
            self.reset_counters()

            self.do_pass(
                PostProcessor,
                False,
                self.import_manager,
                self.scope_manager,
                self.def_manager,
                self.class_manager,
                self.module_manager,
            )


            if iter_cnt in [0]:
                ns_to_be_remove = set()
                for ns1, defi1 in self.def_manager.defs.items():
                    if defi1.get_type() == utils.constants.EXT_DEF and '.' in ns1:

                        ext_class = ns1.rsplit('.', 1)[0]
                        ext_method = ns1.split('.')[-1]
                        for ns2, defi2 in self.def_manager.defs.items():
                            if defi2.get_type() == utils.constants.CLS_DEF and utils.equal_attribute(ext_class, ns2):

                                if ns2 + '.' + ext_method in self.def_manager.defs:
                                    pass
                                else:
                                    ns_to_be_remove.add(ns1)

                for ns in ns_to_be_remove:
                    self.def_manager.remove(ns)  
             

            self.def_manager.complete_definitions()
            iter_cnt += 1

            '''print(iter_cnt, "后处理完成")
            print("____________________________________")
            print("____________________________________")
            print("____________________________________")'''

        self.reset_counters()

        '''print("后处理完成")
        print("____________________________________")
        print("____________________________________")
        print("____________________________________")'''

        #in_modules = self.module_manager.get_internal_modules
        #for in_module in in_modules:
        #    print(in_module)

        '''scope = self.scope_manager.get_scope('examples\\abode2\\devices\\light.Light.set_color_temp')
        print(scope.fullns)
        defi = scope.defs.get('response')
        print(defi.fullns)
        point = defi.points_to.get('name')
        print(point)
        val = point.values
        val.discard('state.Stateful._client.send_request')
        val.add('examples\\abode2\\client.Client.send_request')



        def2 = self.def_manager.defs['examples\\abode2\\devices\\light.Light.set_color_temp.response']
        print(def2.fullns)
        point2 = defi.points_to.get('name')
        print(point2)
        val2 = point.values
        val2.discard('state.Stateful._client.send_request')
        val2.add('examples\\abode2\\client.Client.send_request')'''

        #self.scope_manager.get_scope('examples\\abode2\\devices\\light.Light.set_color_temp').defs.get('response').points_to.get('name').values.discard('state.Stateful._client.send_request')
        #self.scope_manager.get_scope('examples\\abode2\\devices\\light.Light.set_color_temp').defs.get('response').points_to.get('name').values.add('examples\\abode2\\client.Client.send_request')

        #valSet = defi.points_to.get('name').values
        #for val in valSet:
            #print(val)
        #defi.points_to.get('name').

        typeInfer = TypeInference(self.class_manager, self.scope_manager, self.def_manager)


        #Comment out the following one line to disable the type inference feature
        typeInfer.generate()
        attribute_matching_to_class = typeInfer._attribute_matching_to_class
        methods = typeInfer._methods_with_no_path
        attributes = typeInfer._attributes_with_no_path

        dataflow = Dataflow(self.class_manager, self.scope_manager, self.def_manager)


        #Comment out the following three lines to disable the dataflow dependency feature
        dataflow.get_all_methods()
        dataflow.get_assign()
        dataflow.get_return()


        self.cg.add_dataflow_info(dataflow._methods, dataflow._assign_information, 
                                  dataflow._return_information, parameterExtraction._parameters)


        if self.operation == utils.constants.CALL_GRAPH_OP:
            self.do_pass_attribute_matching_to_class(
                CallGraphProcessor,
                False,
                self.import_manager,
                self.scope_manager,
                self.def_manager,
                self.class_manager,
                self.module_manager,
                attribute_matching_to_class,
                methods,
                attributes,
                call_graph=self.cg,
            )
        elif self.operation == utils.constants.KEY_ERR_OP:
            self.do_pass(
                KeyErrProcessor,
                False,
                self.import_manager,
                self.scope_manager,
                self.def_manager,
                self.class_manager,
                self.key_errs,
            )
        else:
            raise Exception("Invalid operation: " + self.operation)

    def output(self):

        self.cg.generate_datacg()

        return self.cg.get()

    def output_key_errs(self):
        return self.key_errs.get()


    def output_edges(self):
        return self.cg.get_edges()

    def _generate_mods(self, mods):
        res = {}
        for mod, node in mods.items():
            res[mod] = {
                "filename": (
                    os.path.relpath(node.get_filename(), self.package)
                    if node.get_filename()
                    else None
                ),
                "methods": node.get_methods(),
            }
        return res

    def output_internal_mods(self):
        return self._generate_mods(self.module_manager.get_internal_modules())

    def output_external_mods(self):
        return self._generate_mods(self.module_manager.get_external_modules())

    def output_functions(self):
        functions = []
        for ns, defi in self.def_manager.get_defs().items():
            if defi.is_function_def():
                functions.append(ns)
        return functions

    def output_classes(self):
        classes = {}
        for cls, node in self.class_manager.get_classes().items():
            classes[cls] = {"mro": node.get_mro(), "module": node.get_module()}
        return classes

    def get_as_graph(self):
        return self.def_manager.get_defs().items()
