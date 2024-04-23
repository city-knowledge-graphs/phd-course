'''
Created on 26 Jan 2021

@author: ejimenez-ruiz
'''
from rdflib import Graph

       

def loadTriplesAndSave():

    #Example from  https://www.stardog.com/tutorials/data-model/
   
    g = Graph()
    g.parse("./data/beatles.ttl", format="ttl")
    
    
    print("The graph contains '" + str(len(g)) + "' triples.")
    
    
        
    #for s, p, o in g:
    #    print((s.n3(), p.n3(), o.n3()))
    
    print("Saving graph to 'beatles.rdf'")
    g.serialize(destination='../student-codes-data/beatles.rdf', format='xml')
    



def loadTriplesAndSaveToTargetFormat(file, target_file, source_format, target_format):

   
    g = Graph()
    g.parse(file, format=source_format)
    
    
    print("The graph contains '" + str(len(g)) + "' triples.")
    
        
    for s, p, o in g:
        print((s.n3(), p.n3(), o.n3()))
    
    print("Saving graph from " + source_format + " to " + target_format)
    #print(g.serialize(format="turtle").decode("utf-8"))
    g.serialize(destination=target_file, format=target_format)


#Load and saves example graph beathles.ttl
loadTriplesAndSave()

#Load triples and save in a given graph
loadTriplesAndSaveToTargetFormat("./data/ernesto_foaf.rdf", "../student-codes-data/ernesto_foaf.ttl", "xml", "ttl")
#loadTriplesAndSaveToTargetFormat("solution/Solution_Task3.1.ttl", "ttl", "xml")
