from rdflib import Graph

import owlrl


def OWLRLInference():
    
    g = Graph()
    
    g.parse("data/example-owl2rl.ttl", format="ttl")
    
    
    print("Loaded '" + str(len(g)) + "' triples.")
    
    #Performs OWL 2 RL  reasoning
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics, axiomatic_triples=True, datatype_axioms=False).expand(g)
    
    
    print("After inference rules: '" + str(len(g)) + "' triples.")
    
    
    #Check if entailments hold
    checkEntailments(g)

    
    print("\nSaving extended graph")
    g.serialize(destination='../student-codes-data/example-owl2rl-extended.ttl', format='ttl')

    


def checkEntailments(g):
    
    print("\nChecking entailments: ")
    
    triple1 = ":Carl :hasChild :Ann ."
    triple2 = ":Ann rdf:type :Child ."
    triple3 = ":Juliet :hasChild :Ann ."
    
    checkEntailment(g, triple1)
    checkEntailment(g, triple2)
    checkEntailment(g, triple3)
    
    
    
    
def checkEntailment(g, triple):
    
    #We use an ASK query instead of a select. It could be done with SELETCT and then checking that the results are not empty 
    qres = g.query(
    """ASK {""" + triple + """ }""")

    #Single row with one boolean vale
    for row in qres:
        print("Does '" + triple + "' hold? " + str(row))
    
    
OWLRLInference()

