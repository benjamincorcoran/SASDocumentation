import random

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import json
from networkx.readwrite import json_graph

from ..SASObjects.SASProgram import SASProgram


class SASFlowChart(object):

    def __init__(self, SASProgram):

        self.G = nx.DiGraph()
        self.G.add_node('start')

        self.SASProgram = SASProgram

        self.nodeLabels = {}
        self.addDataNodes(self.SASProgram.datasteps)
        self.addDataNodes(self.SASProgram.procedures)

        # for obj in self.SASProgram.datasteps:
        #     print('Datastep: ',obj.inputs, obj.outputs)

        # for obj in self.SASProgram.procedures:
        #     print('Procedure: ',obj.procedure,obj.inputs, obj.outputs)

        self.json = json.dumps(json_graph.node_link_data(self.G))

    def addDataNodes(self, SASObject):
        for obj in SASObject:
            for input in obj.inputs:
                inputNode = input.library.upper() + '.' + input.dataset.upper()
                if not input.isNull():
                    if self.G.has_node(inputNode) is False:
                        self.G.add_node(
                            inputNode, lib=input.library.upper(), ds=input.dataset)
                        self.nodeLabels[inputNode] = input.dataset

                    for output in obj.outputs:
                        outputNode = output.library.upper() + '.' + output.dataset.upper()
                        if not output.isNull():
                            if self.G.has_node(outputNode) is False:
                                self.G.add_node(
                                    outputNode, lib=output.library.upper(), ds=output.dataset)
                                self.nodeLabels[outputNode] = output.dataset
                            if hasattr(obj, 'procedure'):
                                if input.dataset != output.dataset:
                                    self.G.add_edge(
                                        inputNode, outputNode, label=obj.procedure)
                            else:
                                if input.dataset != output.dataset:
                                    self.G.add_edge(inputNode, outputNode)

    def countNodes(self):
        return len(list(self.G.nodes()))
