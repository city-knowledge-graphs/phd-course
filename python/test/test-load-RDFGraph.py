'''
Created on 28 Jan 2022

@author: ejimenez-ruiz
'''
from rdflib import Graph

       

def loadTriples(file, format, print_triples):

    #Example from  https://www.stardog.com/tutorials/data-model/
   
    g = Graph()
    g.parse(file, format=format)
    
    
    print("\n\n" + file + " has '" + str(len(g)) + "' triples.")
    
    
    #for stmt in g:    
        #print(stmt)
        
    if print_triples:
        for s, p, o in g:
            print((s.n3(), p.n3(), o.n3()))
        
    return g
    
    
    
def getQueryResults(graph, query):    
    qres = graph.query(query)

    for row in qres:
        print("%s" % row)
        
    
    




#Load triples and query local graph
print("\nLoading beatles.ttl")
graph=loadTriples("beatles.ttl", "ttl", True)
querySoloArtists = """SELECT DISTINCT ?x
       WHERE {
          ?x rdf:type <http://stardog.com/tutorial/SoloArtist> .
       }"""

print("\nQuerying solo artists:")
getQueryResults(graph, querySoloArtists)


	
print("\nTest successful!!")
