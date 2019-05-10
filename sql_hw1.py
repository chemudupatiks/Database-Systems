# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 23:03:01 2019

@author: ckris
"""


import MySQLdb
import csv
from create_schema import returnCreateCommand as rcc
from create_schema import is_number

#returns all the related columns in the string according to the given suffix.
def rrc(s, suffix):
    result = "`"+s+"`"
    if suffix == "etc":
        result+=",`"+ s+"upper`,`"+s+"lower`,`"+"u"+s+"`,`"+s+"ref`,`"+s+"url`,"
    elif suffix == "uletc":
        result+=",`"+ s+"upper`,`"+s+"lower`,`"+"u"+s+"`,`"+s+"ref`,`"+s+"url`,"
    elif suffix =="rurl":
        result+= ",`"+s+"ref`,`"+s+"url`,"
    elif suffix == "ulu":
        result+=",`"+ s+"upper`,`"+s+"lower`,`"+"u"+s+"`,"
    else:
        result+=",`"+suffix+"`,"
    return result

#connects to MySQL
conn = MySQLdb.connect (host = "localhost",
                        user = "user",
                        passwd = "password")
con = conn.cursor()
#creates a database called exoplanets
con.execute("create database if not exists exoplanets")
#changes to exoplanets database
con.execute("use exoplanets")
# drops the exoplanets tables if already exists
try:
    con.execute("drop table exoplanets")
except:
    pass

#gets the create statement and executes it t create a new table called exoplanets.
createC = rcc()
con.execute(createC)

#inserts into table row by row
insert_c = "insert into exoplanets "
ifile = 'exoplanets.csv'
with open(ifile) as inputfile:
   reader = csv.DictReader(inputfile)
   for row in reader:
       first = True
       k = row.keys()
       v = row.values()
       k_c = 0
       v_c = 0
       string_k = "("
       str_v = "("
       for key in k:
           if not first:
               string_k+=','
               str_v+=','
           string_k += "`"+key+"`"
           k_c+=1
           value = row[key]
           if not value:
               str_v+='null'
               v_c+=1
           elif is_number(value):
               str_v+=value
               v_c+=1
           else:
               str_v+='"'+value+'"'
               v_c+=1
           first = False
       string_k+=")"
       str_v+=")"       
       con.execute(insert_c+string_k+" values "+str_v+";")

#drops the two tables planets and stars if they already exist.
try:
    con.execute("drop table stars")
except:
    pass
try:
    con.execute("drop table planets")
except:
    pass

#creates stars 
create_stars = "create table stars as "
stars_col = "(select `stardiscmeth`, `othername`, `jsname`, `epeurl`, `simbadname`, `simbadurl`, `kepid`, `koi`,"\
+ rrc("k","uletc") + "`mult`, `star`,"+rrc("binary", "rurl")+rrc("mstar", "etc")+rrc("rstar", "etc")+rrc("fe", "etc")\
+rrc("teff", "etc")+rrc("rhostar", "etc")+rrc("logg", "etc")+rrc("vsini", "etc")+rrc("gamma", "etc")\
+rrc("v", "rurl")+"`bmv`, `j`, `h`, `ks`, `shk`, `rhk`, `kp`, `specref`, `specurl`, `hipp`, `hd`, `gl`, `hr`, `sao` from exoplanets);"
create_stars+=stars_col
con.execute(create_stars)
#print(create_stars)

#creates planets
create_planets = "create table planets as "
planets_columns = "(select `name`, `star`, `date`, `planetdiscmeth`, `firstref`, `firsturl`, `etdname`,\
 `etdurl`, `eaname`, `eaurl`, `eod`, `microlensing`, `imaging`, `timing`, `astrometry`,"+rrc("msini", "uletc")+rrc("mass", "etc")\
 +rrc("t0", "etc")+rrc("dvdt", "etc")+rrc("lambda", "etc")+rrc("transit", "rurl")+rrc("r", "etc")+rrc("tt", "etc")\
 +rrc("t14", "etc")+rrc("b", "etc")+rrc("ar", "etc")+rrc("depth", "etc")+rrc("density", "etc")+rrc("gravity", "etc")\
 +rrc("dr", "etc")+rrc("rr", "etc")+"trend, ncomp, comp,"+rrc("se", "rurl")+rrc("sedepthj", "etc")+rrc("sedepthh", "etc")\
 +rrc("sedepthks", "etc")+rrc("sedepthkp", "etc")+rrc("sedepth36", "etc")+rrc("sedepth45", "etc")+rrc("sedepth58", "etc")\
 +rrc("sedepth80", "etc")+rrc("set", "etc")+"`ra`, `ra_string`, `dec`, `dec_string`,"+rrc("par", "ulu")+rrc("dist", "etc")\
 +"`orbref`, `orburl`," +rrc("a", "etc")+rrc("sep", "etc")+rrc("per", "etc")\
 +rrc("ecc", "uletc")+rrc("i", "etc")+rrc("om", "etc")+rrc("bigom", "etc")+"`chi2`, `nobs`, `rms`, `freeze_ecc`,"
create_planets+= planets_columns 
create_planets = create_planets +"kde from exoplanets);"
# couldnt find column `month` in the csv 
con.execute(create_planets)
#print("\n\n")
#print(create_planets)
con.execute("alter table planets add primary key (name);")

#closes all connections
con.close()
conn.commit()
conn.close()
