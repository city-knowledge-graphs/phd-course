'''
Created on 20 Mar 2019

@author: ejimenez-ruiz
'''
from enum import Enum


class KG(Enum):
        DBpedia = 0
        Wikidata = 1
        Google = 2        
        All = 3

class URI_KG(object):
    
    dbpedia_uri_resource = 'http://dbpedia.org/resource/'
    
    dbpedia_uri_property = 'http://dbpedia.org/property/'
    
    dbpedia_uri = 'http://dbpedia.org/ontology/'
    wikidata_uri ='http://www.wikidata.org/entity/'
    schema_uri = 'http://schema.org/' 
    
    uris = list()
    uris.append(dbpedia_uri)
    uris.append(wikidata_uri)
    uris.append(schema_uri)
    
    uris_resource = list()
    uris_resource.append(dbpedia_uri_resource)
    uris_resource.append(wikidata_uri)
    
    wikimedia_disambiguation_concept=wikidata_uri+'Q4167410'
    
    
    avoid_predicates=set()
    avoid_predicates.add("http://dbpedia.org/ontology/wikiPageDisambiguates")
    avoid_predicates.add("http://dbpedia.org/ontology/wikiPageRedirects")
    avoid_predicates.add("http://dbpedia.org/ontology/wikiPageWikiLink")
    avoid_predicates.add("http://dbpedia.org/ontology/wikiPageID")
    
    
    #Large amount of text
    avoid_predicates.add("http://dbpedia.org/ontology/abstract")
    avoid_predicates.add("http://www.w3.org/2000/01/rdf-schema#comment")
    
    
    
    
    avoid_predicates.add("http://dbpedia.org/ontology/wikiPageRevisionID")
    avoid_predicates.add("http://dbpedia.org/ontology/wikiPageExternalLink")
    avoid_predicates.add("http://purl.org/dc/terms/subject") #Link to categories
    
    avoid_predicates.add("http://www.w3.org/2000/01/rdf-schema#seeAlso")
    avoid_predicates.add("http://purl.org/linguistics/gold/hypernym")
    avoid_predicates.add("http://xmlns.com/foaf/0.1/primaryTopic")
    #avoid_predicates.add("http://www.w3.org/2002/07/owl#differentFrom")
    #avoid_predicates.add("http://www.w3.org/2002/07/owl#sameAs")
    avoid_predicates.add("http://dbpedia.org/property/related")
    
    
    avoid_top_concepts=set()
    avoid_top_concepts.add("http://www.w3.org/2002/07/owl#Thing")
    avoid_top_concepts.add("http://www.wikidata.org/entity/Q35120") #something
    avoid_top_concepts.add("http://www.wikidata.org/entity/Q830077") #subject 
    avoid_top_concepts.add("http://www.wikidata.org/entity/Q18336849")  #item with given name property 
    avoid_top_concepts.add("http://www.wikidata.org/entity/Q23958946") #individual/instance
    avoid_top_concepts.add("http://www.wikidata.org/entity/Q26720107") # subject of a right 
    avoid_top_concepts.add("http://www.wikidata.org/entity/Q488383") #  object  
    avoid_top_concepts.add("http://www.wikidata.org/entity/Q4406616") #concrete object 
    avoid_top_concepts.add("http://www.wikidata.org/entity/Q29651224") # natural object
    avoid_top_concepts.add("http://www.wikidata.org/entity/Q223557") #physical object 
    avoid_top_concepts.add("http://www.wikidata.org/entity/Q16686022") # natural physical object
    
    
    def __init__(self):
        ''''
        '''
        
        
        



class KGEntity(object):
    
    
    def __init__(self, enity_id, label, description, types, source):
        
        self.ident = enity_id
        self.label = label
        self.desc = description #sometimes provides a very concrete type or additional semantics
        self.types = types  #set of semantic types
        self.source = source  #KG of origin: dbpedia, wikidata or google kg
        
    
    def __repr__(self):
        return "<id: %s, label: %s, description: %s, types: %s, source: %s>" % (self.ident, self.label, self.desc, self.types, self.source)

    def __str__(self):
        return "<id: %s, label: %s, description: %s, types: %s, source: %s>" % (self.ident, self.label, self.desc, self.types, self.source)
    
    
    def getId(self):
        return self.ident
    
    '''
    One can retrieve all types or filter by KG: DBpedia, Wikidata and Google (Schema.org)
    '''
    def getTypes(self, kgfilter=KG.All):
        if kgfilter==KG.All:
            return self.types
        else:
            kg_uri = URI_KG.uris[kgfilter.value]
            filtered_types = set()
            for t in self.types:
                if t.startswith(kg_uri):
                    filtered_types.add(t)
            
            return filtered_types 
    
    def getLabel(self):
        return self.label
    
    def getDescription(self):
        return self.desc
    
    def getSource(self):
        return self.sourcec
    
    
    def addType(self, cls):
        self.types.add(cls)
    
    def addTypes(self, types):
        self.types.update(types)
        
        
        
if __name__ == '__main__':
    print(URI_KG.uris[KG.DBpedia.value])
    print(KG.DBpedia.value)
          
    