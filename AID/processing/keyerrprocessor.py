import ast
import os
import re

import utils
from processing.base import ProcessingBase


class KeyErrProcessor(ProcessingBase):
    def __init__(
        self,
        filename,
        modname,
        import_manager,
        scope_manager,
        def_manager,
        class_manager,
        key_errs,
        modules_analyzed=None,
    ):
        super().__init__(filename, modname, modules_analyzed)
        # parent directory of file
        self.parent_dir = os.path.dirname(filename)

        self.import_manager = import_manager
        self.scope_manager = scope_manager
        self.def_manager = def_manager
        self.class_manager = class_manager
        self.key_errs = key_errs

        self.closured = self.def_manager.transitive_closure()
        self.state = "keyerr"

    def visit_Subscript(self, node):
        self.visit(node.value)
        self.visit(node.slice)
        names = self.retrieve_subscript_names(node)
        for name in names:
            if not self.is_subscriptable(name):
                continue

            defi = self.def_manager.get(name)
            if not defi:
                splitted = name.split(".")

                self.key_errs.add(
                    filename=os.path.relpath(
                        self.filename, self.import_manager.get_mod_dir()
                    ),
                    lineno=node.lineno,
                    namespace=".".join(splitted[:-1]),
                    key=splitted[-1],
                )

    def is_subscriptable(self, name):
        if re.match(r".*<dict[0-9]+>.*", name):
            return True

        return False

    def analyze_submodules(self):
        super().analyze_submodules(
            KeyErrProcessor,
            self.import_manager,
            self.scope_manager,
            self.def_manager,
            self.class_manager,
            self.key_errs,
            modules_analyzed=self.get_modules_analyzed(),
        )

    def analyze(self):
        self.visit(ast.parse(self.contents, self.filename))
        self.analyze_submodules()

    def visit_Lambda(self, node):
        counter = self.scope_manager.get_scope(self.current_ns).inc_lambda_counter()
        lambda_name = utils.get_lambda_name(counter)
        utils.join_ns(self.current_ns, lambda_name)

        super().visit_Lambda(node, lambda_name)
