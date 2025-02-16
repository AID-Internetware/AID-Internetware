import utils

class CallGraph(object):
    def __init__(self):
        self.cg = {}
        self.modnames = {}

        self._return_information = {}
        self._assign_information = {}

        self.datacg = {}
        self.enhancedcg = {}

    def add_dataflow_info(self, methods_info, assign_info, return_info, parameter_info):       
        
        #self._methods = set()
        self._methods = methods_info
        self._assign_information = assign_info
        self._return_information = return_info
        #(parameter, method)
        self._parameter_information = parameter_info
     

    def add_node(self, name, modname=""):
        if not isinstance(name, str):
            raise CallGraphError("Only string node names allowed")
        if not name:
            raise CallGraphError("Empty node name")

        if name not in self.cg:
            self.cg[name] = set()
            self.modnames[name] = modname

        if name in self.cg and not self.modnames[name]:
            self.modnames[name] = modname

    def add_edge(self, src, dest):
        self.add_node(src)
        self.add_node(dest)
        self.cg[src].add(dest)

    def get(self):

        return self.enhancedcg

    def get_edges(self):
        output = []
        for src in self.cg:
            for dst in self.cg[src]:
                output.append([src, dst])
        return output

    def get_modules(self):
        return self.modnames
    

    def generate_datacg(self):
        for key, value in self._assign_information.items():
            if utils.common.is_method_node(key, self._methods):
                visited = set()
                queue = [key]
                while queue:
                    current_node = queue.pop(0)
                    if current_node not in visited:
                        visited.add(current_node)
                        if utils.common.is_method_node(current_node, self._methods) and current_node != key:
                            if current_node not in self.datacg:
                                self.datacg[current_node] = set()
                            self.datacg[current_node].add(key)
                        elif current_node in self._parameter_information and current_node != key:
                            if self._parameter_information[current_node] not in self.datacg:
                                self.datacg[self._parameter_information[current_node]] = set()
                            self.datacg[self._parameter_information[current_node]].add(key)
                        else:
                            queue.extend(self._assign_information.get(current_node, []))
                            queue.extend(self._return_information.get(current_node, []))
        for key, value in self._return_information.items():
            if utils.common.is_method_node(key, self._methods):
                visited = set()
                queue = [key]
                while queue:
                    current_node = queue.pop(0)
                    if current_node not in visited:
                        visited.add(current_node)
                        if utils.common.is_method_node(current_node, self._methods) and current_node != key:
                            if current_node not in self.datacg:
                                self.datacg[current_node] = set()
                            self.datacg[current_node].add(key)
                        elif current_node in self._parameter_information and current_node != key:
                            if self._parameter_information[current_node] not in self.datacg:
                                self.datacg[self._parameter_information[current_node]] = set()
                            self.datacg[self._parameter_information[current_node]].add(key)
                        else:
                            queue.extend(self._assign_information.get(current_node, []))
                            queue.extend(self._return_information.get(current_node, []))

        for key in self.cg.keys() | self.datacg.keys():
            self.enhancedcg[key] = self.cg.get(key, set()) | self.datacg.get(key, set())

        all_nodes = set()
        for k,v in self.enhancedcg.items():
            all_nodes.add(k)
            all_nodes.union(v)

        equal_dict = dict()
        for n1 in all_nodes:
            for n2 in all_nodes:
                if n1 != n2 and ('.' in n1 and '.' in n2) and ('\\' in n1 or '\\' in n2):
                    v1 = n1.replace('\\', '.')
                    v2 = n2.replace('\\', '.')
                    if v1 != v2 and v1 in v2 and v2.split(v1)[-1] == '':
                        equal_dict[n1] = n2
                    elif v1 != v2 and v2 in v1 and v1.split(v2)[-1] == '':
                        equal_dict[n2] = n1

        for value in self.enhancedcg.values():
            for key in equal_dict.keys():
                if key in value:
                    value.remove(key)
                    value.add(equal_dict[key])


        for k,v in equal_dict.items():
            if k in self.enhancedcg.keys() and v in self.enhancedcg.keys() and self.enhancedcg[k] == self.enhancedcg[v]:
                self.enhancedcg.pop(k)


        rules1_answer = set()
        rules2_answer = set()

        
        for end in utils.constants.NETWORK_PROTOCOL_METHODS_LIST:
            if end in self.enhancedcg:
                #print(end)

                reverse_cg = self.reverse_graph(self.enhancedcg)
                temp = self.api_identification(reverse_cg, end)
                #print(len(temp))   
                result1 = set([x for x in temp if "\\" in x and "._" not in x])
                #print(len(result1))
                #for k,v in self.reverse_graph(self.enhancedcg).items():
                #    print(k,v)
                    
                result2 = set(self.get_result2(self.enhancedcg, reverse_cg, result1))

                rules1_answer = rules1_answer | result1
                rules2_answer = rules2_answer | result2

        rules12_answer = rules1_answer | rules2_answer

        final_answer = {item for item in rules12_answer if "\\__main__" not in item}
        print("API number:" + str(len(final_answer)))
        for i in final_answer:
            print(i)


    def judge_connection(self, start, end, visited=None, path=None):

        if visited is None:
            visited = set()
        if path is None:
            path = []

        visited.add(start)
        path = path + [start]

        def is_equal(v1: str, v2: str):
            if v1 == v2:
                return True
            v1 = v1.replace('\\', '.')
            v2 = v2.replace('\\', '.')
            if v1 in v2 and v2.split(v1)[-1] == '':
                return True
            elif v2 in v1 and v1.split(v2)[-1] == '':
                return True
            else:
                return False

        if start == end:
            return True

        for neighbor in self.enhancedcg.get(start, []):
            if neighbor not in visited:
                if self.judge_connection(neighbor, end, visited, path):
                    return True

        return False
    
    def reverse_graph(self, graph):
        reverse = {}
        for node, neighbors in graph.items():
            for neighbor in neighbors:
                if neighbor not in reverse:
                    reverse[neighbor] = []
                reverse[neighbor].append(node)
        return reverse

    def api_identification(self, call_graph, node):
        source_nodes = []
    
        def dfs(current_node, visited):
            visited.add(current_node)
            if current_node not in call_graph:
                source_nodes.append(current_node)
                return
            for next_node in call_graph[current_node]:
                if next_node not in visited:
                    dfs(next_node, visited)
        
        dfs(node, set())
        return source_nodes
    
    def get_result2(self, call_graph, reverse_cg, result1):
        result2 = []
        for root_node in result1:
            for child_node in call_graph[root_node]:
                if len(reverse_cg[child_node]) == 1 and "\\" in child_node and "._" not in child_node and "<" not in child_node:
                    result2.append(child_node)
        
        return result2
    
        

class CallGraphError(Exception):
    pass
