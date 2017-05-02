#Precision and Recall
import pandas as pd
import csv
from collections import defaultdict
import operator

csv_file_1="C:/Users/Shruti Jadon/Desktop/DatabaseProject/PrecisionRecall/First.csv"
csv_file_2="C:/Users/Shruti Jadon/Desktop/DatabaseProject/PrecisionRecall/Second.csv"
csv_file_3="C:/Users/Shruti Jadon/Desktop/DatabaseProject/PrecisionRecall/Manual_Mapping.csv"
def extract_file(csv_file):
    df = pd.read_csv(csv_file) #you can also use df['column_name']
    test_attribute= df['test_attribute'].tolist()
    train_attribute=df['train_attribute'].tolist()
    i=0
    Matched_Dictionary={}
    Matched_Dictionary[test_attribute[i]]=train_attribute[i]
    for i in range(0,len(test_attribute)-1):
        if(test_attribute[i]!=test_attribute[i+1]):
            Matched_Dictionary[test_attribute[i+1]]=train_attribute[i+1]

    return Matched_Dictionary


def extracted_files(csv_file):
    df = pd.read_csv(csv_file) #you can also use df['column_name']
    test_attribute= df['test_attribute'].tolist()
    train_attribute=df['train_attribute'].tolist()
    probability=df['probability']
    temp_dictionary=defaultdict(list)
    i=0
    temp_dictionary[test_attribute[i]].append((probability[i],train_attribute[i]))
    for i in range(0,len(test_attribute)-1):
        if(test_attribute[i]==test_attribute[i+1]):
            temp_dictionary[test_attribute[i]].append((probability[i],train_attribute[i]))
        else:
            temp_dictionary[test_attribute[i]].append((probability[i],train_attribute[i]))
    dict_1=defaultdict(list)
    dict_2={}
    dict_3={}
    for keys in temp_dictionary.keys():
        #print keys +":::::"
        x= temp_dictionary[keys]
        for values in range(0,len(x)):
            dict_1[keys].append(x[values][1])
    #return dict_1, dict_2, dict_3
    return dict_1  
    
First=extracted_files(csv_file_1)
#print First
Second=extracted_files(csv_file_2)
Manual=extract_file(csv_file_3)

#precision calculation false positive and false negative
#false positive is something that shouldn't have been matched but is matching
#false negative is something that should have been null but is matched
# true positive is perfectly matched ones
#precision= tp/tp+fp
#recall= tp/tp+fn
#matching is false p when highest is not same as manual one. 
#false negative if it is present in list

def F1score(evaluation_file,manual_file):
    tp=0
    fp=0
    fn=0
    max_len=len(evaluation_file.keys())
    #print max_len
    for e_key in evaluation_file.keys():
        #print "evaulation of keys"
        for m_key in manual_file.keys():
            if(e_key==m_key):
                if(manual_file[m_key]==evaluation_file[e_key][0]):
                    tp=tp+1
                elif (manual_file[m_key]!=evaluation_file[e_key][0]):
                    fp=fp+1
                else:
                    for values in evaluation_file[e_key]:
                        if(manual_file[m_key]==evaluation_file[e_key][values]):
                            fn=fn+1
    precision=(tp*1.0)/(tp+fp)
    recall=(tp*1.0)/(tp+fn)
    F1_Score=(2*precision*recall)/(precision+recall)
    second_score=tp*1.0/max_len
    return F1_Score, second_score
    
print F1score(First,Manual)

print F1score(Second,Manual)

                    
                    
    
    
    
    




