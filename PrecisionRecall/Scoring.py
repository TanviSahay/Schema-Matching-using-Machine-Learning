#Precision and Recall
import pandas as pd
import csv


csv_file_1="C:/Users/Shruti Jadon/Desktop/DatabaseProject/PrecisionRecall/First.csv"
csv_file_2="C:/Users/Shruti Jadon/Desktop/DatabaseProject/PrecisionRecall/Second.csv"
csv_file_3="C:/Users/Shruti Jadon/Desktop/DatabaseProject/PrecisionRecall/Manual_Mapping.csv"
def extract_file(csv_file):
    df = pd.read_csv(csv_file) #you can also use df['column_name']
    column_names = list(df.columns.values)
    test_attribute= df['test_attribute'].tolist()
    train_attribute=df['train_attribute'].tolist()
    i=0
    Matched_Dictionary={}
    Matched_Dictionary[test_attribute[i]]=train_attribute[i]
    for i in range(0,len(test_attribute)-1):
        if(test_attribute[i]!=test_attribute[i+1]):
            Matched_Dictionary[test_attribute[i+1]]=train_attribute[i+1]

    return Matched_Dictionary

First=extract_file(csv_file_1)
Second=extract_file(csv_file_2)
Manual=extract_file(csv_file_3)

#precision calculation false positive and false negative
#false positive is something that shouldn't have been matched but is matching
#false negative is something that should have been null but is matched
# true positive is perfectly matched ones
#precision= tp/tp+fp
#recall= tp/tp+fn

def F1score(evaluation_file,manual_file):
    tp=0
    fp=0
    fn=0
    max_len=len(manual_file.keys())
    for e_key in evaluation_file.keys():
        #print "evaulation of keys"
        for m_key in manual_file.keys():
            if(e_key==m_key):
                if(manual_file[m_key]==evaluation_file[e_key]):
                    tp=tp+1
                    #print manual_file[m_key]
                    #print evaluation_file[e_key]
                elif(manual_file[m_key]==""):
                    fn=fn+1
                else:
                    fp=fp+1
    #print tp
    precision=tp*1.0/(tp+fp)
    recall=tp*1.0/(tp+fn)
    F1_Score=(2*precision*recall)/(precision+recall)
    second_score=tp*1.0/max_len
    return F1_Score, second_score

print F1score(First,Manual)
print F1score(Second,Manual)
                    
                    
    
    
    
    




