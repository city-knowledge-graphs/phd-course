'''
Created on 26 Jan 2021

@author: ejimenez-ruiz
'''
from rdflib import Graph
from rdflib import URIRef, BNode, Literal
from rdflib import Namespace
from rdflib.namespace import OWL, RDF, RDFS, FOAF, XSD

#DOCUMENTATION: 
#https://rdflib.readthedocs.io/en/stable/intro_to_creating_rdf.html
#https://rdflib.readthedocs.io/en/stable/rdf_terms.html

def createTriples():
    
    #Empty graph
    g = Graph()
    
    #Special namspaces to create  
    city = Namespace("http://www.example.org/university/london/city#")
    dbpo = Namespace("http://dbpedia.org/ontology/")
       
    #Prefixes
    g.bind("foaf", FOAF) #FOAF is given as defaulty namespace
    g.bind("city", city) #city is a newly created namespace
    g.bind("dbpo", dbpo) #dbpo is a newly created namespace 
    
    #These lines are equivalent:    
    #ernesto = URIRef("http://www.example.org/university/london/city#ernesto")
    #city.ernesto
    
    #print(city.ernesto)
    
    bnode = BNode()  # a GUID is generated

    name = Literal('Ernesto Jimenez-Ruiz', datatype=XSD.string)  # lang="en" for language tags
    year = Literal('2024', datatype=XSD.gYear)  # lang="en" for language tags
   

    g.add((city.inm713, RDF.type, city.Module))
    g.add((city.ernesto, RDF.type, city.Lecturer))
    
    g.add((city.Lecturer, RDFS.subClassOf, FOAF.Person))
    
    g.add((city.ernesto, FOAF.name, name))
    g.add((city.ernesto, city.teaches, city.inm713))
    
    g.add((bnode, RDF.type, RDF.Statement ))
    g.add((bnode, RDF.subject, city.ernesto ))
    g.add((bnode, RDF.predicate, city.teaches ))
    g.add((bnode, RDF.object, city.inm713 ))
    g.add((bnode, dbpo.year, year ))
    
    
    
    
    print("Saving graph to 'example_rdflib.ttl':")
    
    print(g.serialize(format="turtle").encode("utf-8"))    
    g.serialize(destination='../student-codes-data/example_rdflib.ttl', format='ttl')


createTriples()

