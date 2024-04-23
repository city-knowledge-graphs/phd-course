'''
Created on 17 Feb 2022

@author: ejimenez-ruiz
'''

from SPARQLWrapper import SPARQLWrapper, JSON
import time


def queryRemoteGraph(endpoint_url, query, attempts=3):
   

    #Remote service
    sparqlw = SPARQLWrapper(endpoint_url)        
    sparqlw.setReturnFormat(JSON)
    
       
    try:
            
        sparqlw.setQuery(query)
            
        results = sparqlw.query().convert()
        
        #Prints JSON file
        #print(results)
                   
    
        #Processes the returned JSON with results
        for result in results["results"]["bindings"]:
            
            #Prints individual results. Note that "x" is the variable given in the SPARQL query
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
print("\nQuerying DBPedia Knowledge Graph (semantic types (classes) of Chicago Bulls)")
queryRemoteGraph(dbpedia_endpoint, dbpedia_query)


print("\n\n");
        
dbpedia_query2 = "PREFIX foaf: <http://xmlns.com/foaf/0.1/> PREFIX dbo: <http://dbpedia.org/ontology/> SELECT DISTINCT ?x WHERE { ?jd foaf:name \"Johnny Depp\"@en . ?m dbo:starring ?jd .?m dbo:starring ?other . ?other foaf:name ?x . FILTER (STR(?x)!=\"Johnny Depp\")} ORDER BY ?x  LIMIT 10"
print("Querying DBPedia Knowledge Graph (Some actors co-starring with Johnny Depp)")
queryRemoteGraph(dbpedia_endpoint, dbpedia_query2)





