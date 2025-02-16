class EnhancedCallGraph(object):
    def __init__(self, cg: dict):
        self.cg = cg
        self.ecg = cg
        #self.modnames = {}

    def add_node(self, name):
        if not isinstance(name, str):
            raise EnhancedCallGraphError("Only string node names allowed")
        if not name:
            raise EnhancedCallGraphError("Empty node name")

        if name not in self.cg:
            self.cg[name] = set()
            #self.modnames[name] = modname

        #if name in self.cg and not self.modnames[name]:
            #self.modnames[name] = modname

    def add_edge(self, src, dest):
        self.add_node(src)
        self.add_node(dest)
        self.cg[src].add(dest)

    def get(self):
        return self.cg

    def get_edges(self):
        output = []
        for src in self.cg:
            for dst in self.cg[src]:
                output.append([src, dst])
        return output

    #def get_modules(self):
        #return self.modnames


class EnhancedCallGraphError(Exception):
    pass
