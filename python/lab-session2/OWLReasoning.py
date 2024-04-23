from rdflib import Graph

import owlrl


def OWLRLInference():
    
    g = Graph()
    
    #g.parse("http://protege.stanford.edu/ontologies/pizza/pizza.owl")
    g.parse("data/example-owl2rl.ttl", format="ttl")
    
    print("Loaded '" + str(len(g)) + "' triples.")
    
    #Performs OWL 2 RL  reasoning
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics, axiomatic_triples=True, datatype_axioms=False).expand(g)
    
    
    print("After inference rules: '" + str(len(g)) + "' triples.")
    
        
    print("\nSaving extended graph")
    g.serialize(destination='../student-codes-data/example-owl2rl-extended.ttl', format='ttl')
    


    
    
OWLRLInference()

