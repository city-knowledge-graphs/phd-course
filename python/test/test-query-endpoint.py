'''
Created on 19 Jan 2021

@author: ejimenez-ruiz
'''

from SPARQLWrapper import SPARQLWrapper, JSON
import time


def queryRemoteGraph(endpoint_url, query, attempts=3):
    
    sparqlw = SPARQLWrapper(endpoint_url)        
    sparqlw.setReturnFormat(JSON)
    
       
    try:
            
        sparqlw.setQuery(query)
            
        results = sparqlw.query().convert()
        
        #Prints JSON file
        #print(results)
                   
    
        for result in results["results"]["bindings"]:
            
            #Prints individual results 
            print(result["x"]["value"])
             
             
        
        
    except:
            
        print("Query '%s' failed. Attempts: %s" % (query, str(attempts)))
        time.sleep(60) #to avoid limit of calls, sleep 60s
        attempts-=1
        if attempts>0:
            return queryRemoteGraph(endpoint_url, query, attempts)
        else:
            return None



#Query a remote RDF graph (e.g., SPARQL endpoint)
dbpedia_endpoint = "http://dbpedia.org/sparql"
dbpedia_query = "SELECT DISTINCT ?x WHERE { <http://dbpedia.org/resource/Chicago_Bulls> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?x . }"


print("\nQuerying DBPedia Knowledge Graph (types of Chicago Bulls)")
queryRemoteGraph(dbpedia_endpoint, dbpedia_query)


print("\nTest successful!!")

