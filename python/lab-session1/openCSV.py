import csv
import pandas as pd



def using_builtin_libary(file):
     
     with open(file) as csv_file:
            
        csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"', escapechar="\\")
        
        #previous_key=""    
        
        for row in csv_reader:
            print(row)
            
            
            
def using_pandas(file):
    
    data_frame = pd.read_csv(file, sep=',', quotechar='"',escapechar="\\")    
    
    for cell in data_frame['Company']:
        print(cell)
    
    for row in data_frame.itertuples(index=True, name='Pandas'):
        print(row)
        




using_builtin_libary("./data/companies_file.csv")
using_pandas("./data/companies_file.csv")
