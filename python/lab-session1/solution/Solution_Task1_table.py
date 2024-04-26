from rdflib import Graph
from rdflib import URIRef, BNode, Literal
from rdflib import Namespace
from rdflib.namespace import OWL, RDF, RDFS, FOAF, XSD
from rdflib.util import guess_format
import pandas as pd



class Task2_4_Solution(object):
    '''
    Example of for Lab 2 task 2.4 
    '''
    def __init__(self):
        
         #1. GRAPH INITIALIZATION
    
        #Empty graph
        self.g = Graph()
        
        #Example namespace for this lab
        self.aau_ns_str= "http://www.semanticweb.org/ernesto/aau/"
        
        #Special namspaces class to create directly URIRefs in python.           
        self.aau = Namespace(self.aau_ns_str)
        
        #Prefixes for the serialization
        self.g.bind("aau", self.aau)
        
        
        #Load data in dataframe  
        self.file="../data/companies_file.csv"
        self.data_frame = pd.read_csv(self.file, sep=',', quotechar='"',escapechar="\\")
        
    
    
    def cellToURI(self, cell_name):
        if cell_name.lower() in self.stringToURI:  #Is cell in dictionary
            return self.stringToURI[cell_name.lower()]
        else:
            return self.aau_ns_str + cell_name
    
        
    def solution(self):
        
        #This solution assumes the manual or automatic mapping of the CSV file to a KG like DBPedia
        # Such that:
        #- Column 0 elements are of type https://dbpedia.org/ontology/Company
        #- Column 2 elements are of type https://dbpedia.org/ontology/City
        #- Columns 0 and 1 are related via the predicate https://dbpedia.org/ontology/foundingYear
        #- Columns 0 and 2 are related via the predicate https://dbpedia.org/ontology/headquarter
        # The KG also contains the following entities that can be reused from the KG:
        #http://dbpedia.org/resource/Oxford
        #http://dbpedia.org/resource/London
        #http://dbpedia.org/resource/DeepMind
        #http://dbpedia.org/resource/Oxbotica               

        #Manual mapping. Tip: google the entity name + dbpedia: e.g. "Oxford DBpedia" and get the URI 
        #from the suggested DBPedia page.
        #Automatic mapping: More in week 5. Typically using a fuzzy search (aka look-up) over the KG.
        
        #In this lab I'm just creating a very small dictionary with entities (to be used as a very basic look-up)
        #In Week 5 we will use DBPedia look-up service that provides a fuzzy search functionality
        self.stringToURI = dict()
        self.stringToURI["oxford"]="http://dbpedia.org/resource/Oxford"
        self.stringToURI["london"]="http://dbpedia.org/resource/London"
        self.stringToURI["deepmind"]="http://dbpedia.org/resource/DeepMind"
        self.stringToURI["oxbotica"]="http://dbpedia.org/resource/Oxbotica"
        
         
        
        #DBPedia namspaces
        dbo = Namespace("http://dbpedia.org/ontology/")        
        dbr = Namespace("http://dbpedia.org/resource/")
       
        #Prefixes
        self.g.bind("dbo", dbo)        
        #Alternative: g.bind("dbo", "http://dbpedia.org/ontology/")        
        self.g.bind("dbr", dbr)    
        #We can the use  as entities: dbo.Company or URIRef(http://dbpedia.org/ontology/)

                
        #Iterates over CSV/data frame and creates triples
        #Format csv file        
        #0         1               2
        #"Company","Founding year","Headquarters"                        
        for row in self.data_frame.itertuples(index=False):
            
            #We check if entity in our small local dictionary 
            col0_entity = URIRef(self.cellToURI(row[0]))
            col2_entity = URIRef(self.cellToURI(row[2]))
            
            #Year column
            col1_literal = Literal(row[1], datatype=XSD.gYear)
            
            # We create types
            self.g.add((col0_entity, RDF.type, dbo.Company))
            self.g.add((col2_entity, RDF.type, dbo.City))
            
            #Relationship between col0 and col2
            self.g.add((col0_entity, dbo.headquarter, col2_entity))
            
            #Relationship between col0 and col1
            self.g.add((col0_entity, dbo.foundingYear, col1_literal))
            
         
        
        print("Saving graph to 'Solution_Task1_table.ttl':")
    
        #print(self.g.serialize(format="turtle").decode("utf-8"))    
        self.g.serialize(destination='../../student-codes-data/Solution_Task1_table.ttl', format='ttl')



if __name__ == '__main__':
    
    task2_4 = Task2_4_Solution()
    task2_4.solution()
