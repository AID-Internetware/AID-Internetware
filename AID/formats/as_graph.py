from .base import BaseFormatter


class AsGraph(BaseFormatter):
    def __init__(self, cg_generator):
        self.cg_generator = cg_generator

    def generate(self):
        graph = self.cg_generator.get_as_graph()
        output = {}
        for key, defi in graph:
            output[key] = list(defi.get_name_pointer().get().copy())
        return output
