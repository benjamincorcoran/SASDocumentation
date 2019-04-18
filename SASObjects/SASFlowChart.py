import random

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import json
from networkx.readwrite import json_graph

from SASObjects.SASProgram import SASProgram

class SASFlowChart(object):

    def __init__(self, SASProgram):

        self.figure=plt.figure(figsize=(8,5))

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

        for node in self.G.nodes():
            if len(list(self.G.predecessors(node))) == 0:
                self.G.add_edge('start',node)



    def saveFig(self,path):
        try:
            self.pos = self._hierarchy_pos(self.G,'start')
            self.G.remove_node('start')

            self.nodeColors = list(set([value for key,value in dict(nx.get_node_attributes(self.G,'lib')).items()]))
            cmap = plt.get_cmap('Pastel2')
            colors = cmap(np.linspace(0, 1, len(self.nodeColors)))
            self.nodeColors = dict(zip(self.nodeColors, colors))

            colorList = [self.nodeColors[value] for key,value in dict(nx.get_node_attributes(self.G,'lib')).items()]

            nx.draw_networkx_nodes(self.G,pos=self.pos,alpha=0.8,node_size=100,node_color=colorList)
            nx.draw_networkx_edges(self.G,pos=self.pos,alpha=0.4)
            nx.draw_networkx_labels(self.G,pos=self.pos,labels=self.nodeLabels,font_size=8)
    
            self.edge_labels = nx.get_edge_attributes(self.G,'label')
            self.edge_labels = nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels =self.edge_labels,font_size=8,alpha=0.4)
            
            for _,lab in self.edge_labels.items():
                lab.set_rotation('horizontal')

            legendHandles = [mpatches.Patch(color=value, label=key) for key, value in self.nodeColors.items()]

            plt.legend(handles=legendHandles,fontsize=8)
            plt.axis('off')
        except :
            print("Failed to produce diagram, recursive loop detected.")
        self.figure.savefig(path,format='PNG')
        plt.close()

    def addDataNodes(self,SASObject):
        for obj in SASObject:
            for input in obj.inputs:
                inputNode = input.library.upper()+'.'+input.dataset.upper()
                if not input.isNull():
                    if self.G.has_node(inputNode) is False:
                        self.G.add_node(inputNode,lib=input.library.upper())
                        self.nodeLabels[inputNode]=input.dataset

                    for output in obj.outputs:
                        outputNode = output.library.upper()+'.'+output.dataset.upper()
                        if not output.isNull():
                            if self.G.has_node(outputNode) is False:
                                self.G.add_node(outputNode,lib=output.library.upper())
                                self.nodeLabels[outputNode]=output.dataset
                            if hasattr(obj,'procedure'):
                                if input.dataset != output.dataset:
                                    self.G.add_edge(inputNode,outputNode,label=obj.procedure)
                            else:
                                if input.dataset != output.dataset:
                                    self.G.add_edge(inputNode,outputNode)


    def _hierarchy_pos(self, G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None):
        if pos is None:
            pos = {root:(xcenter,vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.successors(root))
        if len(children)>0:
            dx = width/len(children) 
            nextx = xcenter - width/2 - dx/2
            for i,child in enumerate(children):
                if child != root:
                    nextx += dx
                    pos = self._hierarchy_pos(G, child, width = dx, vert_gap = vert_gap, 
                                        vert_loc = vert_loc-vert_gap - 0.025*i, xcenter=nextx,
                                        pos=pos, parent = root)
        return pos

    def countNodes(self):
        return len(list(self.G.nodes()))
