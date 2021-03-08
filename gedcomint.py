'''
@authors: Steven Santiago Andrew Antonacci Alex Waldron
We pledge our Honor that we have abided by the Stevens Honor System.
'''
from prettytable import PrettyTable

class Individual:
    def __init__(self, id):
        self.id = id
        self.name = ""
        self.birthday = ""
        self.age = ""
        self.alive = True
        self.death = ""
        self.child = "N/A"
        self.spouse = "N/A"
        self.gender = ""
        self.famc = ""
        self.fams = []
        

class Family():
    def __init__(self, id):
        self.id = id
        self.married = "" 
        self.divorced = "N/A"
        self.husbandID = ""
        self.husbandName = ""
        self.wifeID = ""
        self.wifeName = "" 
        self.children = []

indiv = []
fams = []

def readfil():
    filename = "dataSet.ged"
    valid_tags = ["INDI", "NAME", "SEX", "BIRT", "DEAT", "FAMC","FAMS","FAM", "MARR", "HUSB", "WIFE", "CHIL", "DIV", "DATE", "HEAD", "TRLR", "NOTE"]

    with open(filename) as f:
        content = f.read().splitlines()
    d = Individual(0)

    f = Family(0)
    dateb = False
    dated = False
    datem = False
    datev = False
    for line in content:
        i = 0
        print("--> " + line)
        sep = line.split(" ")
        s = "<-- "
        for x in sep:
            if i==0 :
                s += x + "|"
                i+=1
            elif x == "INDI" or x == "FAM":
                if x == "INDI":
                    indiv.append(d)
                    d = Individual(s[6:-3])
                if x == "FAM":
                    fams.append(f)
                    f = Family(s[6:-3])
                if i == 2:
                    t = s[6:-3]
                    s = s[0:6]
                    s+= x + "|Y|" + t
            elif i ==1 : 
                if x in valid_tags: 
                    s+= x + "|Y|"
                    y = x
                else:
                    s+= x + "|N|"
                i+=1
                if y == "BIRT":
                    dateb = True
                    dated = False
                    datem = False
                    datev = False
                if y == "MARR":
                    dateb = False
                    dated = False
                    datem = True
                    datev = False
                if y == "DIV":
                    dateb = False
                    dated = False
                    datem = False
                    datev = True
                    f.divorced = ""
                if y == "_SEPR":
                    dateb = False
                    dated = False
                    datem = False
                    datev = False
            else:
                s+=x + " "
                if y == "NAME":
                    d.name += x + " "
                if y == "SEX":
                    d.gender = x
                if y == "DEAT":
                    dateb = False
                    dated = True
                    datem = False
                    datev = False
                    d.alive = False
                if y == "DATE":
                    if dateb:
                        d.birthday += x + " "
                    if dated:
                        d.death += x + " "
                    if datem:
                        f.married += x + " "
                    if datev:
                        f.divorced += x + " "
                if y == "FAMC":
                    d.famc = x
                if y == "FAMS":
                    d.fams.append(x)
                if y == "HUSB":
                    f.husbandID = x
                if y == "WIFE":
                    f.wifeID = x
                if y == "CHIL":
                    f.children.append(x)


        print(s)
    calcAges()
    checkParentAge(fams)
    checkMaxAge()
    checkMarriage()
    checkDeath()
    check_duplicate_name_and_birth()
    check_duplicate_spouse_and_marriage_date()
    printData(indiv, fams)
def findMonth(month):
    months = ["JAN", "FEB", "MAR","APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    for mon in months:
        if mon == month:
            return months.index(mon);
    return 0



def check_duplicate_name_and_birth():
    for individual in indiv:
        no_duplicate_name_and_birth(individual, indiv)

def check_duplicate_spouse_and_marriage_date():
    for fam in fams:
        no_duplicate_spouse_and_marriage_date(fam,fams)

def no_duplicate_name_and_birth(individual, all_individuals):
    '''for given individual in all_indivuals determine if there is another indivudal with a duplicate name and birthdate'''
    number_of_name_birth_matches = 0

    for single_individual in all_individuals:
        if (single_individual.name == individual.name) and (single_individual.birthday == individual.birthday):
            
            number_of_name_birth_matches += 1

    if number_of_name_birth_matches > 1:
        print("ERROR: INDIVIDUAL: US23: {}: Individual name ({}) and birthday ({}) duplicate found".format(individual.id, individual.name, individual.birthday))
        return False

    return True

def no_duplicate_spouse_and_marriage_date(family, families):
    number_of_spouse_date_matches = 0
    for fam in families:
      if (fam.married != "") and (fam.wifeName != ""):
        if (fam.married == family.married) and (fam.wifeName == family.wifeName):
            number_of_spouse_date_matches += 1
    if number_of_spouse_date_matches > 1:
        print("ERROR: FAMILY: US24: {}: Family spouse ({}) and marriage date ({}) duplicate found ".format(family.id,family.wifeName, family.married))
        return False
    return True



def largerDate(date1,date2):#returns true if date1 is older than date2
    datea = date1.split(" ")
    dateb = date2.split(" ")
    if datea[2] < dateb[2] :
        return True
    if datea[2] > dateb[2] :
        return False
    if findMonth(datea[1]) < findMonth(dateb[1]):  
        return True
    if findMonth(datea[1]) > findMonth(dateb[1]):  
        return False   
    if datea[0] <= dateb[0] : 
        return True
    else:
        return False

def checkParentAge(fams):
    for fam in fams:
      husb = Individual(0)
      wife = Individual(0)
      children = []
      for individual in indiv:
        if fam.husbandID == individual.id:
          husb = individual
        if fam.wifeID == individual.id:
          wife = individual
        if individual.id in fam.children:
          children.append(individual)
      for child in children:
        try:
          if int(husb.birthday[-4:]) < int(child.birthday[-4:])-80 :
            print("ERROR: FAMILY: US12: {}: FATHER TOO OLD FOR CHILD".format(fam.id))
        except:
          pass
        try:
          if int(wife.birthday[-4:]) < int(child.birthday[-4:])-60 :
            print("ERROR: FAMILY: US12: {}: WIFE TOO OLD FOR CHILD".format(fam.id))
        except:
         pass
def checkMaxAge():
    for individual in indiv:
      try:
        if individual.age >= 150:
          print("ERROR: INDIVIDUAL: US07: {}: INDIVIDUAL TOO OLD".format(individual.id))
      except:
        pass

def calcAges():
    today = "8 MAR 2021"
    todate = today.split(" ")
    for individual in indiv:
        if individual.birthday != "":    
            birthdate = individual.birthday.split(" ")
            if (individual.alive):
                age = int(todate[2]) - int(birthdate[2])
                if findMonth(todate[1]) < findMonth(birthdate[1]) :
                    age -=1
                elif findMonth(todate[1]) == findMonth(birthdate[1]) :
                    if int(todate[0])<int(birthdate[0]):
                        age -= 1
            else:
                deathdate = individual.death.split(" ")
                age = int(deathdate[2]) - int(birthdate[2])
                if findMonth(deathdate[1]) < findMonth(birthdate[1]) :
                    age -=1
                elif findMonth(deathdate[1]) == findMonth(birthdate[1]) :
                    if int(deathdate[0])<int(birthdate[0]):
                        age -= 1
            individual.age = age

def checkMarriage():
    for family in fams:
        for individual in indiv:
            if individual.id == family.husbandID:
                if individual.birthday == "" or family.married == "":
                    pass
                else: 
                    if not largerDate(individual.birthday, family.married):
                        print("ERROR: FAMILY: US02: {}: HUSBAND BORN BEFORE MARRIAGE".format(family.id))
            if individual.id == family.wifeID:
                if individual.birthday == "" or family.married == "":
                    pass
                else: 
                    if not largerDate(individual.birthday, family.married):
                        print("ERROR: FAMILY: US02: {}: WIFE BORN BEFORE MARRIAGE".format(family.id))
def checkDeath():
    for individual in indiv:
      if not individual.alive :
        try: 
          if largerDate(individual.deathdate,individual.birthdate):
            print("ERROR: INDIVIDUAL: US03: {}: DEAD BEFORE BIRTH".format(individual.id))
        except:
          pass
def printData(individuals, families):
    ''' Receive list of Individual objects and Family objects as parameters, print
    and save output to output.txt'''
    today = "22 FEB 2021"
    todate = today.split(" ")
    individualTable = PrettyTable()
    individualTable.field_names = [
                                 'ID', 'Name', 'Gender', 'Birthday', 'Age', 'Alive',
                                 'Death','Child','Spouse'
                                 ]
    for individual in individuals:
        
        individualTable.add_row([
                             individual.id, individual.name, individual.gender,
                             individual.birthday, individual.age, individual.alive,
                             individual.death, individual.child, individual.spouse
                             ])
    
    familyTable = PrettyTable()
    familyTable.field_names = [
                               'ID', 'Married', 'Divorced', 'Husband ID', 'Husband Name',
                             'Wife ID', 'Wife Name', 'Children'
                             ]
    for family in families:
        for individual in individuals:
            if individual.id == family.husbandID:
                family.husbandName = individual.name
            if individual.id == family.wifeID:
                family.wifeName = individual.name
        familyTable.add_row([
                          family.id, family.married, family.divorced, family.husbandID,
                          family.husbandName, family.wifeID, family.wifeName, 
                          family.children
                        ])
        
    print('Individuals')
    print(individualTable)
    print('Families')
    print(familyTable)

    output = open('output.txt', 'w')
    output.write(
        'Individuals\n' + individualTable.get_string() + '\nFamilies\n' + familyTable.get_string()
        )
    output.close()

if __name__ == '__main__':
    readfil()
