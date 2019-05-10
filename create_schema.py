#!/usr/bin/python    
# revised on the given code given by Dr.Ruben Gamboa
import csv

def is_number(s):
    try:
        float(s + "0")
        return True
    except ValueError:
        return False

def returnCreateCommand():
    
    create_command = ""
    ifile = 'exoplanets.csv'
    
    
    collen = {}
    with open(ifile) as inputfile:
       reader = csv.DictReader(inputfile)
       first = True
       line = 1
       for row in reader:
#          print(row.values(), "\n\n")
          
          line = line + 1
          k = row.keys()
          for item in k:
              if first:
                  collen[item] = 0
              else:
                  if row[item] != '\\N':
                      if collen[item] > 0 or not is_number(row[item]):
                          if collen[item] < len(row[item]):
                              collen[item] = len(row[item])
        
    #      if (first): print("\n\ncollen:", collen, "\n\n")
          first = False
          
    
    #print("\n\ncollen:", collen, "\n\n")
              
    
    create_command = create_command + 'create table exoplanets ('
    with open(ifile) as inputfile:
       reader = csv.DictReader(inputfile)
       for row in reader:
          first = True
          k = row.keys()
          for item in k:
             if collen[item] == 0:
                sqltype = "double"
             else:
                sqltype = "VARCHAR(" + str(collen[item]) + ")"
             if not first:
                create_command = create_command + ','
             create_command = create_command + '`' + item + '` ' + sqltype
             first = False;
          break
       create_command = create_command + ')'
        
    return create_command


