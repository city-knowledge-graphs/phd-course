'''
Created on 19 Jan 2021

@author: ejimenez-ruiz
'''
from owlready2 import *


def loadOntology(urionto):
    
    #Method from owlready
    onto = get_ontology(urionto).load()
    
    
    for cls in onto.classes():
        #if "http://dbpedia.org/ontology/" in cls.iri:            
        print("\t"+cls.iri)
    
    print("Classes in pizza-owl: " + str(len(list(onto.classes()))))


#Load ontology
#urionto="http://www.cs.ox.ac.uk/isg/ontologies/dbpedia.owl"
urionto="pizza.owl"
loadOntology(urionto)

print("\nTest successful!!")
