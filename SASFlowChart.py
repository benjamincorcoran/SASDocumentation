import networkx as nx
import matplotlib.pyplot as plt
from SASObjects.SASProgram import SASProgram

if __name__=='__main__':

    G = nx.DiGraph()
    path = 'W:\SASDocumentation\donottrack\\TEFmaps - TEF Pilot 2018-19 - Subject_Level.sas'
    parsedSASFile = SASProgram(path)

    for ds in parsedSASFile.datasteps:
        for input in ds.inputs:
            if G.has_node(input.dataset) is False:
                G.add_node(input.dataset)
            for output in ds.outputs:
                if G.has_node(output.dataset) is False:
                    G.add_node(output.dataset)
                G.add_edge(input.dataset,output.dataset)
    
    nx.draw_spring(G, with_labels=True)
    plt.show()