#
# Copyright (c) 2020 Vitalis Salis.
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
import utils

class CallGraph(object):
    def __init__(self):
        self.cg = {}
        self.modnames = {}

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
        all_nodes = set()
        for k,v in self.cg.items():
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

        for value in self.cg.values():
            for key in equal_dict.keys():
                if key in value:
                    value.remove(key)
                    value.add(equal_dict[key])


        for k,v in equal_dict.items():
            if k in self.cg.keys() and v in self.cg.keys() and self.cg[k] == self.cg[v]:
                self.cg.pop(k)
 

        rules1_answer = set()
        rules2_answer = set()

        for end in utils.constants.NETWORK_PROTOCOL_METHODS_LIST:
            if end in self.cg:

                reverse_cg = self.reverse_graph(self.cg)

                temp = self.api_identification(reverse_cg, end)

                result1 = set([x for x in temp if "\\" in x and "._" not in x])

                    
                result2 = set(self.get_result2(self.cg, reverse_cg, result1))

                rules1_answer = rules1_answer | result1
                rules2_answer = rules2_answer | result2


        rules12_answer = rules1_answer | rules2_answer

        final_answer = {item for item in rules12_answer if "\\__main__" not in item}
        print("API number:" + str(len(final_answer)))
        for i in final_answer:
            print(i)

        return self.cg

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
                if len(reverse_cg[
                           child_node]) == 1 and "\\" in child_node and "._" not in child_node and "<" not in child_node:
                    result2.append(child_node)

        return result2

    def get_edges(self):
        output = []
        for src in self.cg:
            for dst in self.cg[src]:
                output.append([src, dst])
        return output

    def get_modules(self):
        return self.modnames


class CallGraphError(Exception):
    pass
