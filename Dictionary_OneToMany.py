import pickle, csv, os, re, numpy


Global_Dictionary={}
Global_Dictionary[('Name')]=['First Name','Last Name','First_Name','Last_Name','FName','LName','F_Name','L_Name']
Global_Dictionary[('Address','Location','Addr','Residence', 'Loc')]=['Street Name','S_Name','St_Name', 'Str_Name','Stree_Name','StName', 'St_No','ST_Number','Street_No','S_No','S_Number','Street Number', 'StNumber','StNo','Apt_Num','Apartment_Number','Apartment Number','Apartment No','Apt_Number', 'Apt_No']
Global_Dictionary[('SUB-1_%')]=['S_SUB-1_%','*',0.01]
Global_Dictionary[('TOB-1_%')]=['S_TOB-1_%','*',0.01]
Global_Dictionary[('TOB-2_%')]=['S_TOB-2_%','*',0.01]
Global_Dictionary[('TOB-2a_%')]=['S_TOB-2a_%','*',0.01]
Global_Dictionary[('FUH-30_%')]=['S_FUH-30_%','*',0.01]
Global_Dictionary[('FUH-7_%')]=['S_FUH-7_%','*',0.01]
Global_Dictionary[('IMM-2_%')]=['S_IMM-2_%','*',0.01]

print Global_Dictionary.keys()

##Check the schema attribute name with the keys and values in the dictionary (both the actual value and the lower case value).  



