import psycopg2 as db
import psycopg2.extras
import FeatureExtraction as fe
import pickle

FLOATISH_TYPES = (700, 701, 1700)   		  # real, float8, numeric - 0
INT_TYPES = (20, 21, 23)  					  # bigint, int, smallint - 1
CHAR_TYPES = (25, 1042, 1043,)  			  # text, char, varchar   - 2
BOOLEAN_TYPES = (16,)  						  # bool                  - 3
DATE_TYPES = (1082, 1114, 1184, )  			  # date, timestamp, timestamptz - 4
TIME_TYPES = (1083, 1114, 1184, 1266,)        # time, timestamp, timestamptz, timetz - 5

keys = ['PRIMARY KEY' , 'FOREIGN KEY']

features = ['type','length','key','unique','not_null','avgUsedLength','VarofLength','VarCoeffLength','average','variance','Coeff','min','max','whitespace','specialchar','num2all','char2all','backslash','brackets','hyphen']
        
conn = db.connect("dbname='databaseproject' user='tanvi'")
n_data = 1644
typ = 'tr_'
#n_data = 52
#typ = 'ts_'

curs = conn.cursor()

curs.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' ;")

tab = curs.fetchall()

table_nam = ''.join(tab[0])

curs = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


curs.execute('Select *from ' + table_nam +' limit 20;')

descr = curs.description # description about the column attributes

     
attributes = {}
for i in range (0,len(descr)):
      attributes[descr[i][0]] = []
      
      if descr[i][1] in FLOATISH_TYPES:
           attributes[descr[i][0]].append(0)  # storing type - real/float/numeric of attribute
      
      if descr[i][1] in INT_TYPES:
           attributes[descr[i][0]].append(1)  # storing type - int of attribute
           
      if descr[i][1] in CHAR_TYPES:
           attributes[descr[i][0]].append(2)  # storing type - char of attribute
           
      if descr[i][1] in BOOLEAN_TYPES:
           attributes[descr[i][0]].append(3)  # storing type - boolean of attribute
           
      if descr[i][1] in DATE_TYPES:
           attributes[descr[i][0]].append(4)  # storing type - date of attribute
           
      if descr[i][1] in TIME_TYPES:
           attributes[descr[i][0]].append(5)  # storing type - time of attribute
      
      attributes[descr[i][0]].append(descr[i][3])  # storing length of attribute
                                  
'''
int - text - text - text-

(Column(name='pubid', type_code=23, display_size=None, internal_size=4, precision=None, scale=None, null_ok=None),  
 Column(name='pubkey', type_code=25, display_size=None, internal_size=-1, precision=None, scale=None, null_ok=None), 
 Column(name='title', type_code=25, display_size=None, internal_size=-1, precision=None, scale=None, null_ok=None), 
 Column(name='year', type_code=25, display_size=None, internal_size=-1, precision=None, scale=None, null_ok=None))
 
 
curs.execute("select constraint_type from information_schema.table_constraints where table_name='publications';")
 
all_modifiers = curs.fetchall()


PRIMARY KEY
 UNIQUE
 CHECK
 
create table test ( ssn NUMERIC(10) PRIMARY KEY, Emp_id character(10) UNIQUE , Address character(100) not null);
 
#SELECT * FROM pg_constraint WHERE conrelid = 'publications'::regclass::oid

#pg_dump -s dblp -t publications > db.sql

'''

# This command is giving the list of constraints - Keys, Unique, check on all the columns of a table.
curs.execute("SELECT tc.constraint_type, tc.table_name, kcu.column_name FROM information_schema.table_constraints tc LEFT JOIN information_schema.key_column_usage kcu ON tc.constraint_catalog = kcu.constraint_catalog AND tc.constraint_schema = kcu.constraint_schema AND tc.constraint_name = kcu.constraint_name;")

modifiers_column = curs.fetchall()

# This command is extracting keys and unique from the above list.
constraint_column = []
for i in range (0,len(modifiers_column)) :
     if modifiers_column[i][0] == 'PRIMARY KEY' or modifiers_column[i][0] ==  'FOREIGN KEY' or modifiers_column[i][0] == 'UNIQUE':
         constraint_column.append(modifiers_column[i])
        

#print constraint_column

# Append 0 for Primary and Foreign Key , then update as we find the column in the list.
for i in range (0,len(descr)):
    attributes[descr[i][0]].append(0)

for i in range(0,len(constraint_column)):
    if constraint_column[i][0] in keys:
       attributes[constraint_column[i][2]][-1] = 1 # storing Primary / Foreign Key of attribute  
 
# Append 0 for Unique Constraint , then update as we find the column in the list.
for i in range (0,len(descr)):
    attributes[descr[i][0]].append(0)
    
for i in range(0,len(constraint_column)):         
    if constraint_column[i][0] == 'UNIQUE':
       attributes[constraint_column[i][2]][-1] = 1 # storing Unique constraint of attribute     
 
 
# This command is giving the list of nullable constraints on all the columns of a table.
curs.execute("select column_name, IS_NULLABLE from INFORMATION_SCHEMA.COLUMNS where table_name ='"+ table_nam +"';") 
Null_attributes = curs.fetchall()  

# Append 0 for Not_Null attribute, then update as we find the column in the list.
for i in range (0,len(descr)):
    attributes[descr[i][0]].append(0)
    
for i in range (0,len(Null_attributes)):
         if Null_attributes[i][1] == 'NO':
            attributes[Null_attributes[i][0]][-1] = 1 # storing Not-null constraint of attribute   - it cannot be null  
        
#print attributes   

curs = conn.cursor()

for i in range (0,len(descr)):
        curs.execute('Select ' + descr[i][0] + ' from ' + table_nam + ';')
        #data = curs.fetchall()
        data = list(zip(*curs.fetchall())[0])
        #print type(data)
        temp = []
        # Converting the date format to mm/dd/yyyy
        if attributes[descr[i][0]][0] == 4 :
            for j in range (0,len(data)):
                temp.append(data[j].strftime('%m/%d/%Y'))
        
            data = temp  
        fixed_length=attributes[descr[i][0]][1] 
        attributes[descr[i][0]].append(float(fe.averageusedlength(data,n_data,fixed_length)))
        print 'average used length - ', fe.averageusedlength(data, n_data, fixed_length)

        attributes[descr[i][0]].append(fe.varianceoflength(data,fixed_length))
        attributes[descr[i][0]].append(fe.varianceCoefflength(data))
        if attributes[descr[i][0]][0] == 1 or attributes[descr[i][0]][0] == 0:
            number_features=list(fe.numFeatures(data,fixed_length,n_data))
       	    for values in number_features:
      	          attributes[descr[i][0]].append(values)
            attributes[descr[i][0]].append(0.0)
            attributes[descr[i][0]].append(0.0)
            attributes[descr[i][0]].append(0.0)
            attributes[descr[i][0]].append(0.0)
            attributes[descr[i][0]].append(0.0)
            attributes[descr[i][0]].append(0.0)
            attributes[descr[i][0]].append(0.0)
        else:	
            attributes[descr[i][0]].append(0.0)
            attributes[descr[i][0]].append(0.0)
            attributes[descr[i][0]].append(0.0)
            attributes[descr[i][0]].append(0.0)	
            attributes[descr[i][0]].append(0.0)	
            attributes[descr[i][0]].append(fe.WhiteSpaceFeature(data))
            attributes[descr[i][0]].append(fe.specialChars(data))
            attributes[descr[i][0]].append(fe.NumbertoAll(data))
            attributes[descr[i][0]].append(fe.ChartoAll(data))
            attributes[descr[i][0]].append(fe.Numberofbackslash(data))
            attributes[descr[i][0]].append(fe.Numberofbrackets(data))
            attributes[descr[i][0]].append(fe.Numberofhyphen(data))

#for key,values in attributes.items():
    #print key,values

print attributes['state']


new_attributes = {}
for k in attributes.keys():
    key_val = typ + k
    new_attributes[key_val] = attributes[k]

print new_attributes
pickle.dump(new_attributes,open("../Feature_Vectors/DataFeatures_Train.pickle",'wb'))

print len(new_attributes)

