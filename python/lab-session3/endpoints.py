'''
Created on 19 Mar 2019

@author: ejimenez-ruiz
'''
import time

from SPARQLWrapper import SPARQLWrapper, JSON
from entity import URI_KG
import sys


class SPARQLEndpoint(object):
    '''
    classdocs
    '''
    def __init__(self, endpoint_url):
        '''
        Constructor
        '''
        #"http://dbpedia.org/sparql"
        #Solution when getting 403 errors:
        #https://www.mediawiki.org/wiki/Topic:V1zau9rqd4ritpug
        self.sparqlw = SPARQLWrapper(endpoint_url,      
                    agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
        
        
        
        self.sparqlw.setReturnFormat(JSON)
        
        
    def getSameEntities(self, ent):
        
        query = self.createSPARQLQuerySameAsEntities(ent)
        
        
        return self.getQueryResultsArityOne(query)
    
    
    
    def getEnglishLabelsForEntity(self, ent):
        
        query = self.createEnglishLabelsForURI(ent)
        
        return self.getQueryResultsArityOne4Literals(query)
    
    
        
    def getEntitiesForType(self, cls, offset=0, limit=1000):
        
        query = self.createSPARQLEntitiesForClass(cls, offset, limit)
        
        #print(query)
        
        return self.getQueryResultsArityOne(query)
    
    
    def getEntitiesLabelsForType(self, cls, offset=0, limit=1000):
        
        query = self.createSPARQLEntitiesLabelsForClass(cls, offset, limit)
        
        #print(query)
        
        #Second element is a string so we do not filter it
        return self.getQueryResultsArityTwo(query, True, False)
    
        
    def getTypesForEntity(self, entity):
        
        query = self.createSPARQLQueryTypesForSubject(entity)
        
        return self.getQueryResultsArityOne(query)
    

    def getAllTypesForEntity(self, entity):
        
        query = self.createSPARQLQueryAllTypesForSubject(entity)
        
        return self.getQueryResultsArityOne(query)
        

    def getEquivalentClasses(self, uri_class):
        
        query = self.createSPARQLQueryEquivalentClasses(uri_class)
        
        return self.getQueryResultsArityOne(query)
    
    def getAllSuperClasses(self, uri_class):
        
        query = self.createSPARQLQueryAllSuperClassesForClass(uri_class)
        
        return self.getQueryResultsArityOne(query)
    
    
    def getDistanceToAllSuperClasses(self, uri_class):
        
        query = self.createSPARQLQueryDistanceToAllSuperClassesForClass(uri_class)
             
        super2dist = self.getQueryResultsArityTwo(query, False, False)
        
        #Filter top classes   
        for top_cls in URI_KG.avoid_top_concepts:
            super2dist.pop(top_cls, None)
    
    
        return super2dist
    
    
    
    def getAllSubClasses(self, uri_class):
        
        query = self.createSPARQLQueryAllSubClassesForClass(uri_class)
        
        return self.getQueryResultsArityOne(query)
    
    
    def getDistanceToAllSubClasses(self, uri_class, max_level=-1):
        
        query = self.createSPARQLQueryDistanceToAllSubClassesForClass(uri_class)
             
        sub2dist = self.getQueryResultsArityTwo(query, False, False)
        
        if max_level>0:
            sub2dist_new = sub2dist.copy()
            for scls in sub2dist.keys():
                #Only one element in set
                if int(sorted(sub2dist_new[scls])[0])>max_level:
                    sub2dist_new.pop(scls)
                
            return sub2dist_new
        else:
            return sub2dist
            
        
    
    
    def getPredicatesForSubject(self, subject_entity, limit=1000):
        
        query = self.createSPARQLQueryPredicatesForSubject(subject_entity, limit)
        
        return self.getQueryResultsArityOne(query)
        
    def getPredicatesForObject(self, obj_entity, limit=1000):
        
        query = self.createSPARQLQueryPredicatesForObject(obj_entity, limit)
        
        return self.getQueryResultsArityOne(query)   
    
    
    
    #Exploits the domain types of the properties
    def getTypesUsingPredicatesForSubject(self, subject_entity, limit=1000):
        
        query = self.createSPARQLQueryDomainTypesOfPredicatesForSubject(subject_entity, limit)
        
        return self.getQueryResultsArityOne(query)
        
    #Exploits the range types of the properties
    def getTypesUsingPredicatesForObject(self, obj_entity, limit=1000):
        
        query = self.createSPARQLQueryRangeTypesOfPredicatesForObject(obj_entity, limit)
        
        return self.getQueryResultsArityOne(query)   
    
    
    
    def getTopTypesUsingPredicatesForSubject(self, subject_entity, limit=5):
        
        query = self.createSPARQLQueryDomainTypesCountOfPredicatesForSubject(subject_entity, limit)
        
        return self.getQueryResultsArityOne(query)
        
    #Exploits the range types of the properties
    def getTopTypesUsingPredicatesForObject(self, obj_entity, limit=5):
        
        query = self.createSPARQLQueryRangeTypesCountOfPredicatesForObject(obj_entity, limit)
        
        return self.getQueryResultsArityOne(query)   
    
    
    
    def getTriplesForSubject(self, subject_entity, limit=1000):
        
        query = self.createSPARQLQueryTriplesForSubject(subject_entity, limit)
        
        #print(query)        
        #print(self.getQueryResultsArityTwo(query, False, False))
        
        return self.getQueryResultsArityTwo(query, False, False)
        
        
    def getTriplesForObject(self, obj_entity, limit=1000):
        
        query = self.createSPARQLQueryTriplesForObject(obj_entity, limit)
        
        return self.getQueryResultsArityTwo(query)    
    
    
    def getSomeValuesForPredicate(self, predicate, limit=100):
        
        query = self.createSPARQLQuerySomeValuesForPredicate(predicate, limit)
        
        return self.getQueryResultsArityOne(query)    
        
        
        
    
    
    def getQueryResults(self, query, attempts=5):
        
        try:
            
            self.sparqlw.setQuery(query)
            
            return self.sparqlw.query().convert()
        
        except Exception as e:
            
            print("Query '%s' failed. Attempts: %s" % (query, str(attempts)))
            print("\t" + str(e))
            time.sleep(60) #to avoid limit of calls, sleep 60s
            attempts-=1
            if attempts>0:
                return self.getQueryResults(query, attempts)
            else:
                return None


    def getQueryResultsArityOne(self, query, filter_uri=True):
        
        
        results = self.getQueryResults(query, 3)
            
            
        result_set = set()
    
        if results==None:
            print("None results for", query)
            return result_set
            
    
        for result in results["results"]["bindings"]:
            #print(result)
            #print(result["uri"]["value"])
            uri_value = result["uri"]["value"]
            
            if not filter_uri or uri_value.startswith(URI_KG.dbpedia_uri) or uri_value.startswith(URI_KG.wikidata_uri) or uri_value.startswith(URI_KG.schema_uri) or uri_value.startswith(URI_KG.dbpedia_uri_resource) or uri_value.startswith(URI_KG.dbpedia_uri_property): 
                result_set.add(uri_value)
        
        
        return result_set
    
    
    
    def getQueryResultsArityOne4Literals(self, query):
        
        
        results = self.getQueryResults(query, 3)
            
            
        result_set = set()
    
        if results==None:
            print("None results for", query)
            return result_set
            
    
        for result in results["results"]["bindings"]:
            
            value = result["literal"]["value"]
            
            result_set.add(value)
        
        
        return result_set
    
    
    
    
    def getQueryResultsArityTwo(self, query, filter_outA=True, filter_outB=True):
        
        #self.sparqlw.setQuery(query)
        #results = self.sparqlw.query().convert()

        results = self.getQueryResults(query, 3)
    
        result_dict = dict()
        
        if results==None:
            print("None results for", query)
            return result_dict
        
    
        for result in results["results"]["bindings"]:
            #print(result)
            #print(result["uri"]["value"])
            outA_value = result["outA"]["value"]
            outB_value = result["outB"]["value"]
            
            
            if not filter_outA or outA_value.startswith(URI_KG.dbpedia_uri) or outA_value.startswith(URI_KG.wikidata_uri) or outA_value.startswith(URI_KG.schema_uri) or outA_value.startswith(URI_KG.dbpedia_uri_resource) or outA_value.startswith(URI_KG.dbpedia_uri_property): 
                
                    if not filter_outB or outB_value.startswith(URI_KG.dbpedia_uri) or outB_value.startswith(URI_KG.wikidata_uri) or outB_value.startswith(URI_KG.schema_uri) or outB_value.startswith(URI_KG.dbpedia_uri_resource) or outB_value.startswith(URI_KG.dbpedia_uri_property):
                        
                        if outA_value not in result_dict:
                            result_dict[outA_value] = set() 
                        
                        result_dict[outA_value].add(outB_value)
                
        
        return result_dict
        
        
 
    
    
    


    def createSPARQLQueryTriplesForObject(self, obj, limit=1000):
        
        props_to_filter=""
        for p in URI_KG.avoid_predicates:
            props_to_filter+="<" + p + ">," 
        props_to_filter = props_to_filter[0:len(props_to_filter)-1]
        
        #props_to_filter = ",".join(URI_KG.avoid_predicates)        
        
        return "SELECT DISTINCT ?outA ?outB WHERE { ?outA ?outB <" + obj + "> . FILTER( ?outB NOT IN("+ props_to_filter+")) } limit " + str(limit)
        
    def createSPARQLQueryTriplesForSubject(self, subject, limit=1000):
        
        props_to_filter=""
        for p in URI_KG.avoid_predicates:
            props_to_filter+="<" + p + ">,"
            #props_to_filter+= p + ", " 
        props_to_filter = props_to_filter[0:len(props_to_filter)-1]
        
        #props_to_filter = ",".join(URI_KG.avoid_predicates)
        
        return "SELECT DISTINCT ?outA ?outB WHERE { <" + subject + "> ?outA ?outB  FILTER( ?outA NOT IN("+ props_to_filter+")) } limit " + str(limit)
        #return "SELECT DISTINCT ?outA ?outB WHERE { <" + subject + "> ?outA ?outB . } limit " + str(limit)
    
    
    def createSPARQLQueryPredicatesForSubject(self, subject, limit=1000):
        return "SELECT DISTINCT ?uri WHERE { <" + subject + "> ?uri [] . } limit " + str(limit)
    
    def createSPARQLQueryPredicatesForObject(self, obj, limit=1000):
        return "SELECT DISTINCT ?uri WHERE { [] ?uri <" + obj + "> . } limit " + str(limit)
    
    
    def createSPARQLQueryDomainTypesOfPredicatesForSubject(self, subject, limit=1000):
        return "SELECT DISTINCT ?uri WHERE { <" + subject + "> ?p [] . ?p rdfs:domain ?uri . } limit " + str(limit)
    
    def createSPARQLQueryRangeTypesOfPredicatesForObject(self, obj, limit=1000):
        return "SELECT DISTINCT ?uri WHERE { [] ?p <" + obj + "> . ?p rdfs:range ?uri . } limit " + str(limit)
    
    
    def createSPARQLQuerySomeValuesForPredicate(self, predicate, limit=100):
        return "SELECT DISTINCT ?uri WHERE { ?s <" + predicate + "> ?uri . } limit " + str(limit)
    
    
    
    #SELECT DISTINCT ?outA COUNT(?outA) as ?outB WHERE { [] ?p <http://dbpedia.org/resource/Scotland> . ?p rdfs:range ?outA . } GROUP BY ?outA ORDER BY DESC(?outB) limit 3
    #SELECT DISTINCT ?outA WHERE { [] ?p <http://dbpedia.org/resource/Scotland> . ?p rdfs:range ?outA . } GROUP BY ?outA ORDER BY DESC(COUNT(?outA)) limit 3
    #SELECT DISTINCT ?outA WHERE { <http://dbpedia.org/resource/Allan_Pinkerton> ?p [] . ?p rdfs:domain ?outA . } GROUP BY ?outA ORDER BY DESC(COUNT(?outA)) limit 3
    #SELECT DISTINCT ?outA COUNT(?outA) as ?outB WHERE { <http://dbpedia.org/resource/Allan_Pinkerton> ?p [] . ?p rdfs:domain ?outA . } GROUP BY ?outA ORDER BY DESC(?outB) limit 3 
    
    def createSPARQLQueryDomainTypesCountOfPredicatesForSubject(self, subject, limit=3):
        return "SELECT DISTINCT ?uri WHERE { <" + subject + "> ?p [] . ?p rdfs:domain ?uri . } GROUP BY ?uri HAVING (COUNT(?uri) > 3) ORDER BY DESC(COUNT(?uri)) limit " + str(limit)
    
    def createSPARQLQueryRangeTypesCountOfPredicatesForObject(self, obj, limit=3):
        return "SELECT DISTINCT ?uri WHERE { [] ?p <" + obj + "> . ?p rdfs:range ?uri . } GROUP BY ?uri HAVING (COUNT(?uri) > 3) ORDER BY DESC(COUNT(?uri)) limit " + str(limit)
    
    
    def createEnglishLabelsForURI(self, uri_subject):
        return "SELECT DISTINCT ?literal WHERE { <" + uri_subject + "> rdfs:label ?literal . FILTER( langMatches(lang(?literal), 'en')) }"
    

class DBpediaEndpoint(SPARQLEndpoint):
    '''
    classdocs
    
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        super().__init__(self.getEndpoint())
        #"http://dbpedia.org/sparql"
       
       
       
    
        
        
    def getEndpoint(self):
        return "http://dbpedia.org/sparql"



    def getWikiPageRedirect(self, uri_entity):
        
        query = self.createSPARQLQueryWikiPageRedirects(uri_entity)        
        return self.getQueryResultsArityOne(query)
    
    
    def getWikiPageRedirectFrom(self, uri_entity):
        
        query = self.createSPARQLQueryWikiPageRedirectsFrom(uri_entity)        
        return self.getQueryResultsArityOne(query)
    
    
    
    def createSPARQLEntitiesForClass(self, class_uri, offset=0, limit=1000):
            
            
        return "SELECT DISTINCT ?uri WHERE { ?uri <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <" + class_uri + "> . } ORDER BY RAND() OFFSET " + str(offset) + " limit " + str(limit)
        #return "SELECT DISTINCT ?uri WHERE { ?uri a dbo:Country . } ORDER BY RAND() limit " + str(limit)
    
    
    
    def createSPARQLEntitiesLabelsForClass(self, class_uri, offset=0, limit=1000):
            
        return "SELECT DISTINCT ?outA ?outB WHERE { ?outA <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <" + class_uri + "> . ?outA rdfs:label ?outB . FILTER( langMatches(lang(?outB), 'en')) } ORDER BY RAND() OFFSET " + str(offset) + " limit " + str(limit)
        #Lang restriction required
        #return "SELECT DISTINCT ?outA ?outB WHERE { ?outA <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <" + class_uri + "> . ?outA rdfs:label ?outB . } ORDER BY RAND() OFFSET " + str(offset) + " limit " + str(limit)
       
    
    
    
    #def createEnglishLabelsForURI(self, uri_subject):
    #    return "SELECT DISTINCT ?literal WHERE { <" + uri_subject + "> rdfs:label ?literal . FILTER( langMatches(lang(?literal), 'en')) }"
        
        

    def createSPARQLQueryTypesForSubject(self, uri_subject):
            
        return "SELECT DISTINCT ?uri WHERE { <" + uri_subject + "> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?uri . }"
    
    
    
    def createSPARQLQueryWikiPageRedirects(self, uri_subject):
            
        return "SELECT DISTINCT ?uri WHERE { <" + uri_subject + "> <http://dbpedia.org/ontology/wikiPageRedirects> ?uri . }"
    
    
    def createSPARQLQueryWikiPageRedirectsFrom(self, uri_object):
            
        return "SELECT DISTINCT ?uri WHERE { ?uri <http://dbpedia.org/ontology/wikiPageRedirects> <" + uri_object + "> . }"
    
     
        
    def createSPARQLQueryAllTypesForSubject(self, uri_subject):
            
        return "SELECT DISTINCT ?uri " \
        + "WHERE {" \
        + "{<" + uri_subject + "> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?dt . " \
        + "?dt <http://www.w3.org/2000/01/rdf-schema#subClassOf>* ?uri " \
        + "}" \
        + "UNION {" \
        + "<" + uri_subject + "> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?uri . " \
        + "}" \
        + "UNION {" \
        + "<" + uri_subject + "> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?dt . " \
        + "?dt <http://www.w3.org/2002/07/owl#equivalentClass> ?uri " \
        + "}" \
        + "}"
        
        
    def createSPARQLQueryEquivalentClasses(self, uri_class):
        return "SELECT DISTINCT ?uri " \
        + "WHERE {" \
        + "{<" + uri_class + "> <http://www.w3.org/2002/07/owl#equivalentClass> ?uri ." \
        + "} " \
        + "UNION " \
        + "{ ?uri <http://www.w3.org/2002/07/owl#equivalentClass> <" + uri_class + "> ." \
        + "} " \
        + "}";
        
        
        
    def createSPARQLQueryDistanceToAllSuperClassesForClass(self, uri_cls):
        return "SELECT  ?outA (count(?mid) as ?outB) " \
        + "WHERE {" \
        + "<"+uri_cls+"> <http://www.w3.org/2000/01/rdf-schema#subClassOf>* ?mid . " \
        + "?mid <http://www.w3.org/2000/01/rdf-schema#subClassOf>+ ?outA . " \
        + "}" \
        + "GROUP BY ?outA";  
        ##+ "values ?uri_subject { <" + uri_subject + "> }" \
        
            
        
    def createSPARQLQueryAllSuperClassesForClass(self, uri_cls):
            
        return "SELECT DISTINCT ?uri " \
        + "WHERE { " \
        + "{<" + uri_cls + "> <http://www.w3.org/2000/01/rdf-schema#subClassOf>* ?uri ." \
        + "}" \
        + "UNION {" \
        + "<" + uri_cls + "> <http://www.w3.org/2002/07/owl#equivalentClass> ?uri ." \
        + "}" \
        + "}"
    
    
    
    def createSPARQLQueryAllSubClassesForClass(self, uri_cls):
        
        return "SELECT DISTINCT ?uri " \
        + "WHERE { " \
        + "{?uri <http://www.w3.org/2000/01/rdf-schema#subClassOf>* <" + uri_cls + "> ." \
        + "}" \
        + "UNION {" \
        + "<" + uri_cls + "> <http://www.w3.org/2002/07/owl#equivalentClass> ?uri ." \
        + "}" \
        + "}"
    
    
    def createSPARQLQueryDistanceToAllSubClassesForClass(self, uri_cls):
        

        return "SELECT  ?outA (count(?mid) as ?outB) " \
        + "WHERE {" \
        + "?mid <http://www.w3.org/2000/01/rdf-schema#subClassOf>* <"+uri_cls+"> . " \
        + "?outA <http://www.w3.org/2000/01/rdf-schema#subClassOf>+ ?mid . " \
        + "}" \
        + "GROUP BY ?outA";  
        ##+ "values ?uri_subject { <" + uri_subject + "> }" \
    
    
        
    def createSPARQLQuerySameAsEntities(self, uri_entity):
        return "SELECT DISTINCT ?uri " \
        + "WHERE {" \
        + "{<" + uri_entity + "> <http://www.w3.org/2002/07/owl#sameAs> ?uri ." \
        + "} " \
        + "UNION {" \
        + "?uri <http://www.w3.org/2002/07/owl#sameAs> <" + uri_entity + "> ." \
        + "} " \
        + "}";
        

class WikidataEndpoint(SPARQLEndpoint):
    '''
    classdocs
    
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        super().__init__(self.getEndpoint())
        #"http://dbpedia.org/sparql"
   
   
   
    #<http://www.wikidata.org/prop/direct/P31> rdf:type equivalent (instance of)
    #<http://www.wikidata.org/prop/direct/P279> rdfs:subclassof equivalent    
        
        
    def getEndpoint(self):
        #return "https://query.wikidata.org/sparql"
        return "https://query.wikidata.org/bigdata/namespace/wdq/sparql"
        

    def createSPARQLEntitiesForClass(self, class_uri, offset=0, limit=1000):
            
        #return "SELECT DISTINCT ?uri WHERE { ?uri <http://www.wikidata.org/prop/direct/P31> <" + class_uri + "> . } ORDER BY RAND() limit " + str(limit)
        return "SELECT DISTINCT ?uri WHERE { ?uri <http://www.wikidata.org/prop/direct/P31> <" + class_uri + "> . } ORDER BY RAND() OFFSET " + str(offset) + " limit " + str(limit)
        
    


    def createSPARQLQueryTypesForSubject(self, uri_subject):
            
        return "SELECT DISTINCT ?uri WHERE { <" + uri_subject + "> <http://www.wikidata.org/prop/direct/P31> ?uri . }"
    
    
    
    
    
    
    
        
    
    
    
        
        
    def createSPARQLQueryAllTypesForSubject(self, uri_subject):
            
        return "SELECT DISTINCT ?uri " \
        + "WHERE {" \
        + "{<" + uri_subject + "> <http://www.wikidata.org/prop/direct/P31> ?dt . " \
        + "?dt <http://www.wikidata.org/prop/direct/P279>* ?uri " \
        + "} " \
        + "UNION {" \
        + "<" + uri_subject + "> <http://www.wikidata.org/prop/direct/P31> ?uri . }" \
        + "}";
        
        
    
    def createSPARQLQueryEquivalentClasses(self, uri_class):
        
        return "SELECT DISTINCT ?uri " \
        + "WHERE {" \
        + "{<" + uri_class + "> <http://www.wikidata.org/prop/direct/P1709> ?uri ." \
        + "} " \
        + "UNION {" \
        + "?uri <http://www.wikidata.org/prop/direct/P2888> <" + uri_class + ">  . " \
        + "} " \
        + "UNION {" \
        + "?uri <http://www.wikidata.org/prop/direct/P1709> <" + uri_class + "> ." \
        + "} " \
        + "UNION {" \
        + "<" + uri_class + "> <http://www.wikidata.org/prop/direct/P2888> ?uri . }" \
        + "}";
        #P1709: equivalent class
        #P2888: exavt match
        
        
        
    ##TODO revise
    def createSPARQLQuerySameAsEntities(self, uri_entity):
        return "SELECT DISTINCT ?uri " \
        + "WHERE {" \
        + "{<" + uri_entity + "> <http://www.wikidata.org/prop/direct/P460> ?uri ." \
        + "} " \
        + "UNION {" \
        + "?uri <http://www.wikidata.org/prop/direct/P460> <" + uri_entity + "> ." \
        + "} " \
        + "}";
        
        
        
    def createSPARQLQueryAllSuperClassesForClass(self, uri_cls):
        
        return "SELECT DISTINCT ?uri " \
        + "WHERE {" \
        + "<" + uri_cls + "> <http://www.wikidata.org/prop/direct/P279>+ ?uri " \
        + "}";
    
    
    def createSPARQLQueryDistanceToAllSuperClassesForClass(self, uri_cls):
        

        return "SELECT  ?outA (count(?mid) as ?outB) " \
        + "WHERE {" \
        + "values ?uri_cls { <" + uri_cls + "> }" \
        + "?uri_cls <http://www.wikidata.org/prop/direct/P279>* ?mid ." \
        + "?mid <http://www.wikidata.org/prop/direct/P279>+ ?outA . " \
        + "}" \
        + "GROUP BY ?uri_cls ?outA";  
    
    
    
    
    def createSPARQLQueryAllSubClassesForClass(self, uri_cls):
        
        return "SELECT DISTINCT ?uri " \
        + "WHERE {" \
        + "?uri <http://www.wikidata.org/prop/direct/P279>+ <" + uri_cls + ">" \
        + "}";
    
    
    def createSPARQLQueryDistanceToAllSubClassesForClass(self, uri_cls):
        

        return "SELECT  ?outA (count(?mid) as ?outB) " \
        + "WHERE {" \
        + "values ?uri_cls { <" + uri_cls + "> }" \
        + "?mid <http://www.wikidata.org/prop/direct/P279>* ?uri_cls ." \
        + "?outA <http://www.wikidata.org/prop/direct/P279>+ ?mid . " \
        + "}" \
        + "GROUP BY ?uri_cls ?outA";  
    
    
    


if __name__ == '__main__':
    
    
    
    ent="http://dbpedia.org/resource/London"
    ep = DBpediaEndpoint()
    #Semantic types or classes
    types = ep.getTypesForEntity(ent)
    print("Found " + str(len(types)) + " types.")
    for type in types:
        print("\t", type, ep.getEnglishLabelsForEntity(type))
    
    #sameas = ep.getSameEntities(ent)
    #print(len(sameas), sameas)
    
    
    ent = "http://www.wikidata.org/entity/Q84"
    ep = WikidataEndpoint()
    #Semantic types or classes
    types = ep.getTypesForEntity(ent)
    print("Found " + str(len(types)) + " types.")
    
    for type in types:
        print("\t", type, ep.getEnglishLabelsForEntity(type))
    
    
    
    
    
