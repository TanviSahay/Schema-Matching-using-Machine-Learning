import psycopg2 as db
import psycopg2.extras
import FeatureExtraction as fe
import pickle

        
conn = db.connect("dbname='databaseproject' user='postgres' host='localhost' password='#edc5tgb'")

curs = conn.cursor()

curs.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' ;")

tab = curs.fetchall()

table_nam = ''.join(tab[0])

curs = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

curs.execute('Select *from ' + table_nam +' limit 20;')

Test_set = [description[0] for description in curs.description]

conn = db.connect("dbname='databaseproject_1' user='postgres' host='localhost' password='#edc5tgb'")

curs = conn.cursor()

curs.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' ;")

tab = curs.fetchall()
table_nam = ''.join(tab[0])

curs = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

curs.execute('Select *from ' + table_nam +' limit 20;')

Train_set = [description[0] for description in curs.description]


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
        


