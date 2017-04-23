import psycopg2 as db
import psycopg2.extras
import FeatureExtraction as fe
import pickle

        
Train_data = open("../Feature_Vectors/DataFeatures_Train.pickle",'r'))

Test_data = open("../Feature_Vectors/DataFeatures_Match.pickle",'r'))

Train_set = [k for k in Train_data.keys()]
Test_set = [k for k in Test_data.keys()]
    
print Train_set , Train_set

Global_Dictionary={}
Global_Dictionary[('Name','PatientName')]=[['First Name','First_Name','FName','F_Name'],['Last_Name','Last Name','LName','L_Name']]
Global_Dictionary[('Address','Location','Addr','Residence', 'Loc')]=[['Street Name','S_Name','St_Name', 'Str_Name','Stree_Name','StName'], ['St_No','ST_Number','Street_No','S_No','S_Number','Street Number', 'StNumber','StNo'],['Apt_Num','Apartment_Number','Apartment Number','Apartment No','Apt_Number', 'Apt_No']]

#print Global_Dictionary.values()[0][0]
OnetoMany={}
for keys in Global_Dictionary.keys():
    values=Global_Dictionary[keys]
    for k in keys:
        for attributes in Train_set:
            if(attributes.lower()==k.lower()):
                OnetoMany[attributes]=[]
                print attributes
                print "has a possibility of adding to"
                for test_attributes in Test_set:
                    for i in range(0,len(values)):
                        for v in values[i]:
                            if(test_attributes.lower()==v.lower()):
                                print test_attributes
                                OnetoMany[attributes].append(test_attributes)

print OnetoMany
        


