import random

import networkx as nx
import matplotlib.pyplot as plt

from SASObjects.SASProgram import SASProgram

class SASDataFlowChart(object):

    def __init__(self, SASProgram):

        self.G = nx.DiGraph()
        self.G.add_node('start')

        self.SASProgram = SASProgram

        self.addDataNodes(self.SASProgram.datasteps)
        self.addDataNodes(self.SASProgram.procedures)

        for node in self.G.nodes():
            if len(list(self.G.predecessors(node))) == 0:
                self.G.add_edge('start',node)

        self.pos = self._hierarchy_pos(self.G,'start')
        self.G.remove_node('start')
        nx.draw(self.G,pos=self.pos,with_labels=True)

        self.edge_labels = nx.get_edge_attributes(self.G,'label')
        self.edge_labels = nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels =self.edge_labels)
        
        for _,lab in self.edge_labels.items():
            lab.set_rotation('horizontal')

    def addDataNodes(self,SASObject):
        for obj in SASObject:
            for input in obj.inputs:
                if self.G.has_node(input.dataset) is False:
                    self.G.add_node(input.dataset,lib=input.library)

                for output in obj.outputs:
                    if self.G.has_node(output.dataset) is False:
                        self.G.add_node(output.dataset,lib=input.library)
                    if hasattr(obj,'procedure'):
                        self.G.add_edge(input.dataset,output.dataset,label=obj.procedure)
                    else:
                        self.G.add_edge(input.dataset,output.dataset)


    def _hierarchy_pos(self, G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None):
        if pos is None:
            pos = {root:(xcenter,vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.successors(root))
    
        if len(children)>0:
            dx = width/len(children) 
            nextx = xcenter - width/2 - dx/2
            for child in children:
                if child != root:
                    nextx += dx
                    pos = self._hierarchy_pos(G, child, width = dx, vert_gap = vert_gap, 
                                        vert_loc = vert_loc-vert_gap, xcenter=nextx,
                                        pos=pos, parent = root)
        return pos

