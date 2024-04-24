from rdflib import Graph



def compareWithReference(reference_mappings_file, system_mappings_file):
    ref_mappings = Graph()
    ref_mappings.parse(reference_mappings_file, format="ttl")
    
    system_mappings = Graph()
    system_mappings.parse(system_mappings_file, format="ttl")
    
    
    #We calculate precision and recall via true positives, false positives and false negatives
    #https://en.wikipedia.org/wiki/Precision_and_recall        
    tp=0
    fp=0
    fn=0
    
    for t in system_mappings:
        if t in ref_mappings:
            tp+=1
        else:
            fp+=1

    
    for t in ref_mappings:
        if not t in system_mappings:
            fn+=1
            
            
    precision = tp/(tp+fp)
    recall = tp/(tp+fn)
    f_score = (2*precision*recall)/(precision+recall)
    #print(tp, tp2)
    #print(fp)
    #print(fn)
    print("Comparing '" + system_mappings_file + "' with '" + reference_mappings_file)
    print("\tPrecision: " + str(precision))
    print("\tRecall: " + str(recall))
    print("\tF-Score: " + str(f_score))
    
    

#P, R, and F can only be obtained if a reference alignment exists.    
compareWithReference("data/anatomy-reference-mappings.ttl", "data/anatomy-example-system-mappings.ttl")

# For the lab you should compare, for example, 
# cmt-confOf-reference.ttl with the cmt-confOf-your-system.ttl you generate.
# compareWithReference("cmt-confOf-reference.ttl", "cmt-confOf-your-system.ttl")

