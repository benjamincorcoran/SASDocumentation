import networkx as nx
import matplotlib.pyplot as plt
from SASObjects.SASProgram import SASProgram

import random


def _hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None):
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
                pos = _hierarchy_pos(G, child, width = dx, vert_gap = vert_gap, 
                                    vert_loc = vert_loc-vert_gap, xcenter=nextx,
                                    pos=pos, parent = root)
    return pos




if __name__=='__main__':

    G = nx.DiGraph()
    path = r'modelSASCode/modelCode.sas'
    parsedSASFile = SASProgram(path)

    G.add_node('start')

    for ds in parsedSASFile.datasteps:
        for input in ds.inputs:
            if G.has_node(input.dataset) is False:
                G.add_node(input.dataset,lib=input.library)

            for output in ds.outputs:
                if G.has_node(output.dataset) is False:
                    G.add_node(output.dataset,lib=input.library)
                G.add_edge(input.dataset,output.dataset)

    for pc in parsedSASFile.procedures:
        
        for input in pc.inputs:
            if G.has_node(input.dataset) is False:
                G.add_node(input.dataset,lib=input.library)
            for output in pc.outputs:
                if G.has_node(output.dataset) is False:
                    G.add_node(output.dataset,lib=input.library)
                G.add_edge(input.dataset,output.dataset,label=pc.procedure)

    for node in G.nodes():
        if len(list(G.predecessors(node))) == 0:
            G.add_edge('start',node)

    pos = _hierarchy_pos(G,'start')
    G.remove_node('start')
    nx.draw(G,pos=pos,with_labels=True)


    # nx.draw(G,pos,labels={node:node for node in G.nodes()})

    edge_labels = nx.get_edge_attributes(G,'label')
    
    edge_labels = nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_labels)
    
    for _,lab in edge_labels.items():
        lab.set_rotation('horizontal')
    plt.show()