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
        



print("\nLoading using csv library: ")
using_builtin_libary("./companies_file.csv")

print("\nLoading using pandas: ")
using_pandas("./companies_file.csv")


print("\nTest successful!!")
