
'''
@authors: Steven Santiago Andrew Antonacci Alex Waldron
We pledge our Honor that we have abided by the Stevens Honor System.
'''
from prettytable import PrettyTable
from datetime import datetime
from dateutil.relativedelta import relativedelta
import unittest
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
    initFams()
    calcAges()
    checkParentAge()
    checkMaxAge()
    checkMarriage()
    checkDeath()
    check_duplicate_name_and_birth()
    check_duplicate_spouse_and_marriage_date()
    checkDivorceBeforeDeath()
    checkDatesBeforeCurrent()
    check_correct_gender_for_role()
    check_unique_famID_indID(fams, indiv)
    checkMarriageBeforeDivorce()
    checkMarriageBeforeDeath()
    check_siblings_married()
    check_child_duplicate()
    checkMaxSiblings()
    checkAllTuplets()
    childBeforeMarriageParent()
    childBeforeDeathParent()
    check_marriage_to_descendants()
    check_first_cousin_marry()
    checkAllTimesBetweenSiblings()
    checkMaleLastNames()
    printData(indiv, fams)
def findMonth(month):
    months = ["JAN", "FEB", "MAR","APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    for mon in months:
        if mon == month:
            return months.index(mon);
    return 0

def checkMaleLastNames():
    check = True
    for fam in fams:
        for child in fam.children:
            if fam.husbandName.split()[-1] != get_individual_at_id(child, indiv).name.split()[-1] and get_individual_at_id(child, indiv).gender == 'M':
                print("ERROR: FAMILY:: US16: {}: Family contains male child with different last name ({})".format(fam.id, child))
                check = False
    return check

def timeBetweenSiblings(fam):
    check = True
    for child in fam.children:
        for child2 in fam.children:
            if child != child2:
                child1Bday = get_individual_at_id(child, indiv).birthday
                child2Bday = get_individual_at_id(child2, indiv).birthday
                if abs(difference_between_dates(child1Bday, child2Bday).days) >= 2 and abs(difference_between_dates(child1Bday, child2Bday).days/30) < 8:
                    check = False
                    print("ERROR: FAMILY: US13: {}: Family contains siblings({},{}) with birthdays >2 days or <8 months apart".format(fam.id, child, child2))
    return check

def checkAllTimesBetweenSiblings():
  check = True
  for fam in fams:
    if not timeBetweenSiblings(fam):
      check = False
  return check

def checkMaxSiblings():
    check = True
    for fam in fams:
        if len(fam.children) >= 15 :

            print("ERROR: FAMILY: US15: {}: Family consists of 15 or greater siblings".format(fam.id))
            check = False
    return check

def countTuplets(fam):
    check = True
    mostBirths = 0
    for child in fam.children:
        tuplets = 1
        for child2 in fam.children:
            if child != child2 and get_individual_at_id(child,indiv).birthday == get_individual_at_id(child2,indiv).birthday:
                tuplets+=1
        if tuplets >= mostBirths:
            mostBirths = tuplets
    if mostBirths > 5:
        print("ERROR: FAMILY: US14: {}: Family consists of more than 5 births on one day".format(fam.id))
        check = False
    return check

def checkAllTuplets():
    check = True
    for fam in fams:
        if not countTuplets(fam):
            check = False
    return check

def check_marriage_to_descendants():
    for family in fams:
        no_marriage_to_descendants(family, fams)

def no_marriage_to_descendants(family, fams):
    husband = family.husbandID
    wife = family.wifeID
    children = family.children
    if (husband is not None) and (wife is not None):
        for fam in fams:
            test_husb = fam.husbandID
            test_wife = fam.wifeID
            for child in children:
                if (test_husb in children) and (test_wife == wife):
                    print(f"ERROR: FAMILY: US17: {fam.id}: Mother ({wife}) married her child ({test_husb})")
                    return False
                    break
                elif (test_wife in children) and (test_husb == husband):
                    print(f"ERROR: FAMILY: US17: {fam.id}: Father ({husband}) married his child ({test_wife})")
                    return False
                    break
    return True

def check_first_cousin_marry(families = fams):
    for fam in families:
        are_first_cousins_married(fam)


def are_first_cousins_married(fam,families = fams):
    
    children = fam.children
    childrens_fams = [get_family_with_husb_wife_id(child,families) for child in children if get_family_with_husb_wife_id(child,families) is not None]
    cousins = [family.children for family in childrens_fams]
    married_cousins = None
    married_cousins_fam_id = None
    num_of_sibling_sets = len(cousins)
    detected_marriages = 0
    for sibling_set1 in cousins:
        for sibling1 in sibling_set1:
            for sibling_set2 in cousins:
                if not sibling_set1 == sibling_set2:
                    for sibling2 in sibling_set2:
                        are_married_result, fam_id = are_married(sibling1, sibling2, families)
                        if are_married_result:
                            married_cousins = [sibling1, sibling2]
                            married_cousins_fam_id = fam_id
    if married_cousins is not None:
        print(f"ERROR: FAMILY: US19: {married_cousins_fam_id}: First cousins {married_cousins[0]} and {married_cousins[1]} are married")
        return True

    return False

def are_married(id1, id2, families = fams):
    
    for fam in families:
        if ((fam.husbandID == id1) and (fam.wifeID == id2)) or ((fam.wifeID == id1) and (fam.husbandID == id2)):    
            return True, fam.id
    else:
        return False, None

def get_family_with_husb_wife_id(husb_wife_id, families):
    
    for family in families:
        if (husb_wife_id == family.husbandID) or (husb_wife_id == family.wifeID):
            return family
            
def months_between_dates(date1, date2):
    date1_datetime = convert_string_to_datetime(date1)
    date2_datetime = convert_string_to_datetime(date2)
    delta = relativedelta(date1_datetime, date2_datetime)
    total_months = abs((delta.years *12) + delta.months)
    return total_months

def difference_between_dates(date1, date2):
    '''returns date1-date2 as datetime object'''
    date1_datetime = convert_string_to_datetime(date1)
    date2_datetime = convert_string_to_datetime(date2)
    return date1_datetime - date2_datetime

def convert_string_to_datetime(date_string):
    date_string_list = date_string.split(' ')[:3]
    date_string = " ".join(date_string_list)
    print(date_string)

    return datetime.strptime(date_string, '%d %b %Y').date()


def check_duplicate_name_and_birth():
    check = True
    for individual in indiv:
        if not no_duplicate_name_and_birth(individual, indiv):
            check = False
    return check

def check_duplicate_spouse_and_marriage_date():
    check = True
    for fam in fams:
        if not no_duplicate_spouse_and_marriage_date(fam,fams):
            check = False
    return check

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

def check_correct_gender_for_role():
    for fam in fams:
        
        correct_gender_for_role(fam,indiv)

def correct_gender_for_role(family, all_individuals):
    ''' for provided family look up husband ID and wife ID and ensure they are male and female '''
    returnDict = {"husbandMale": True, "wifeFemale": True}   
    husband = get_individual_at_id(family.husbandID, all_individuals)
    if husband is not None:
        if husband.gender != 'M':
            returnDict["husbandMale"] = False
            print(f'ERROR: FAMILY: US21: {family.id}: Husband {husband.name} is not a male')

    wife = get_individual_at_id(family.wifeID,all_individuals)
    if wife is not None:
        if wife.gender != 'F':
            
            returnDict["wifeFemale"] = False
            print(f'ERROR: FAMILY: US21: {family.id}: Wife {wife.name} is not a female')

    return returnDict


def check_unique_famID_indID(families, individuals):
    returnDict = {'uniqueFamIDs':True, 'uniqueIndIDs':True}
    
    fam_ids = [family.id for family in families]
    for fam_id in fam_ids:
        if fam_ids.count(fam_id) > 1:
            print(f'ERROR: FAMILY: US22: Duplicate Family ID: {fam_id}')
            returnDict['uniqueFamIDs'] = False


    ind_ids = [individual.id for individual in individuals]
    for ind_id in ind_ids:
        if ind_ids.count(ind_id) > 1:
            print(f'ERROR: INDIVIDUAL: US22: Duplicate Individual ID: {ind_id}')
            returnDict['uniqueIndIDs'] = False

    return returnDict

def check_child_duplicate():
  for fam in fams:
    duplicate_children(fam, indiv)

def duplicate_children(family, individuals):
  children = []
  for childID in family.children :
    children.append(get_individual_at_id(childID, individuals))
  for child1 in children:
    count = 0
    for child2 in children:
      if child1.name.split()[0] == child2.name.split()[0] and child1.birthday == child2.birthday:
        count += 1
      if count > 1:
        print(f"ERROR: FAMILY: US25: Two children have the same first name and date of birth: {child1.name.split()[0]} {child1.birthday}")
        return True 
  return False

def check_siblings_married():
  for fam in fams:
    wifeID = fam.wifeID
    husbandID = fam.husbandID
    are_husb_wife_siblings(wifeID, husbandID, fams)

def are_husb_wife_siblings(wifeID, husbandID, families):
  for family in families:
    if (wifeID in family.children) and (husbandID in family.children):
      print(f"ERROR: FAMILY: US18: Wife ID:{wifeID} and Husband ID:{husbandID} are siblings. Siblings shouldn't marry" )
      return True
  return False

def get_individual_at_id(individual_id, all_individuals):
    
    for individual in all_individuals:
        
        if str(individual.id) == str(individual_id):
            return individual
            break
def childBeforeMarriageParent():
    check1 = True
    check2 = True
    for fam in fams:
        for individual in indiv:
            for child in fam.children:
              if child == individual.id:
                if largerDate(individual.birthday,fam.married):

                    print("ERROR: FAMILY: US08: Child {} was born before marriage in family {}".format(child, fam.id))
                    check1 = False
                if fam.divorced != "N/A":

                    if largerDate(addNineMonths(fam.divorced),individual.birthday):

                        print("ERROR: FAMILY: US08: Child {} was born after 9 months after divroce in family {}".format(child, fam.id))
                        check2 = False
    return check1 or check2

def childBeforeDeathParent():
    check1 = True
    check2 = True
    for fam in fams:
        for individual in indiv:
            if individual.id == fam.wifeID:
                if not individual.alive:
                  for individualc in indiv:
                    for child in fam.children:
                        if child == individualc.id:
                          if largerDate(individualc.birthday,individual.death):
                            print("ERROR: FAMILY: US09: Child {} was born after mother death in family {}".format(child, fam.id))
                            check1 = False
            if individual.id == fam.husbandID:
                if not individual.alive:
                  for individualc in indiv:
                    for child in fam.children:
                      if child == individualc.id:
                        if largerDate(individualc.birthday,addNineMonths(individual.death)):
                            print("ERROR: FAMILY: US09: Child {} was born after 9 months after husband death in family {}".format(child, fam.id))
                            check2 = False

    return check1 or check2

def addNineMonths(date):
    #returns 9 months past the date.
    months = ["JAN", "FEB", "MAR","APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    date9 = date.split(" ")
    if findMonth(date9[1])<=2:
        return "{} {} {}".format(date9[0],months[findMonth(date9[1])+9],date9[2] )
    else:
        year = int(date9[2])
        return "{} {} {}".format(date9[0],months[findMonth(date9[1])-3],year+1)

def marriedAfterFourteen():
    check = True
    for fam in fams:
      husb = Individual(0)
      wife = Individual(0)
      for individual in indiv:
        if fam.husbandID == individual.id:
          husb = individual
        if fam.wifeID == individual.id:
          wife = individual
      try:  
        if int(fam.married[-5:]) <= int(husb.birthday[-5:])+14:
          print("ERROR: FAMILY: US10: {}: Marriage occurred before husband ({}) was 14".format(fam.id, fam.husbandName))
          check = False
        if int(fam.married[-5:]) <= int(wife.birthday[-5:])+14:
          print("ERROR: FAMILY: US10: {}: Marriage occurred before wife ({}) was 14".format(fam.id, fam.wifeName))
          check = False
      except:
        pass
    return check
def checkForBigamy(family):
    check = True
    for fam in fams:
      if (family.husbandID == fam.husbandID) and (family.wifeID != fam.wifeID):
        print("ERROR: INDIVIDUAL: US11: Individual ({}) belongs to more than one family ({}, {})".format(family.husbandName, family.id, fam.id))
        check = False
      if (family.husbandID != fam.husbandID) and (family.wifeID == fam.wifeID):
        print("ERROR: INDIVIDUAL: US11: Individual ({}) belongs to more than one family ({}, {})".format(family.wifeName, family.id, fam.id))
        check = False
    return check
def checkAllForBigamy():
    check = True
    for fam in fams:
      if not checkForBigamy(fam):
          check = False
    return check


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

def checkParentAge():
    check = True
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
          if int(husb.birthday[-5:]) < int(child.birthday[-5:])-80 :
            print("ERROR: FAMILY: US12: {}: FATHER TOO OLD FOR CHILD".format(fam.id))
            check = False
        except:
          pass
        try:
          if int(wife.birthday[-5:]) < int(child.birthday[-5:])-60 :
            print("ERROR: FAMILY: US12: {}: WIFE TOO OLD FOR CHILD".format(fam.id))
            check = False
        except:
         pass
    return check
def checkMaxAge():
    check = True
    for individual in indiv:
      try:
        if individual.age >= 150:
          print("ERROR: INDIVIDUAL: US07: {}: INDIVIDUAL TOO OLD".format(individual.id))
          check = False
      except:
        pass
    return check
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
    check = True
    for family in fams:
        for individual in indiv:
            if individual.id == family.husbandID:
                if individual.birthday == "" or family.married == "":
                    pass
                else: 
                    if not largerDate(individual.birthday, family.married):
                        print("ERROR: FAMILY: US02: {}: HUSBAND BORN BEFORE MARRIAGE".format(family.id))
                        check = False
            if individual.id == family.wifeID:
                if individual.birthday == "" or family.married == "":
                    pass
                else: 
                    if not largerDate(individual.birthday, family.married):
                        print("ERROR: FAMILY: US02: {}: WIFE BORN BEFORE MARRIAGE".format(family.id))
                        check = False
    return check
def initFams():
  for family in fams:
        for individual in indiv:
            if individual.id == family.husbandID:
                family.husbandName = individual.name
            if individual.id == family.wifeID:
                family.wifeName = individual.name

def checkDeath():
    check = True
    for individual in indiv:
      if not individual.alive :
        try: 
          if largerDate(individual.death,individual.birthday):
            print("ERROR: INDIVIDUAL: US03: {}: DEAD BEFORE BIRTH".format(individual.id))
            check = False
        except:
          pass
    return check
def checkMarriageBeforeDivorce():
    check = True
    for family in fams:
        if family.divorced != "N/A":
            if family.married == "":
                print("ERROR: FAMILY: US04: {}: DIVORCE WITHOUT MARRIAGE".format(family.id))
                check = False
            if largerDate(family.divorced, family.married):
                print("ERROR: FAMILY: US04: {}: DIVORCE BEFORE MARRIAGE".format(family.id))
                check = False
            
    return check
def checkMarriageBeforeDeath():
    check = True
    for family in fams:
        if family.married == "":
            continue
        for individual in indiv:
            if individual.id == family.husbandID:
                if individual.alive :
                    pass
                else:
                    if largerDate(individual.death, family.married):
                        print("ERROR: FAMILY: US05: {}: HUSBAND DEATH BEFORE MARRIAGE".format(family.id))
                        check = False
            if individual.id == family.wifeID:
                if individual.alive :
                    pass
                else:
                    if largerDate(individual.death, family.married):
                        print("ERROR: FAMILY: US05: {}: WIFE DEATH BEFORE MARRIAGE".format(family.id))
                        check = False
    return check

def checkDatesBeforeCurrent():
    today = "29 MAR 2021"
    check = 0
    for family in fams:
        if family.married == "":
           pass
        else:
            if largerDate(today, family.married) :
                print("ERROR: FAMILY: US01: {}: MARRIAGE BEFORE CURRENT DATE".format(family.id))
                check +=1
        if family.divorced == "N/A":
           pass
        else:
            if largerDate(today, family.divorced) :
                print("ERROR: FAMILY: US01: {}: DIVORCE BEFORE CURRENT DATE".format(family.id))
                check +=1

    for individual in indiv:
        if individual.birthday == "":
           pass
        else:
            if largerDate(today, individual.birthday) :
                print("ERROR: INDIVIDUAL: US01: {}: BIRTH BEFORE CURRENT DATE".format(individual.id))
                check +=1
        if individual.death == "":
           pass
        else:
            if largerDate(today, individual.death) :
                print("ERROR: INDIVIDUAL: US01: {}: DEATH BEFORE CURRENT DATE".format(individual.id))
                check +=1
    return check
def checkDivorceBeforeDeath():
    check = True
    for family in fams:
        if family.divorced == "N/A":
            pass
        else:
            for individual in indiv:
                if family.husbandID == individual.id:
                    if individual.alive:
                        pass
                    else:
                        if largerDate(individual.death, family.divorced) : 
                            print("ERROR: FAMILY: US06: {}: DEATH BEFORE DIVORCE".format(family.id))
                            check = False
                if family.wifeID == individual.id:
                    if individual.alive:
                        pass
                    else:
                        if largerDate(individual.death, family.divorced) : 
                            print("ERROR: FAMILY: US06: {}: DEATH BEFORE DIVORCE".format(family.id))
                            check = False
    return check

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
class Test(unittest.TestCase):
    readfil()
    def testBirthBeforeMarriage(self): 
        self.assertFalse(checkMarriage() , "There is an individual with an incorrect marriage")
    def testBirthBeforeDeath(self): 
        self.assertFalse(checkDeath() , "There is an individual with an incorrect death date")
    def testDivorceBeforeDeath(self): 
        self.assertFalse(checkDivorceBeforeDeath() , "There is a Family with an incorrect divorce date")
    def testDateBeforeCurrentDate(self): 
        self.assertEquals(checkDatesBeforeCurrent(),2 , "There are 2 individuals/families with an incorrect date")
    def testCheckMaxAge(self):
        self.assertFalse(checkMaxAge() , "There is an Individual who is too old")     
    def testCheckParentAge(self):
        self.assertFalse(checkParentAge() , "There is an Individual who is too old to be a parent")
    def testCheckAllForBigamy(self):
        self.assertFalse(checkAllForBigamy() , "There is an Individual who is in two or more marriages")
    def testMarriedAfterFourteen(self):
        self.assertFalse(marriedAfterFourteen() , "There is an Individual who is married under 15 years old")
    def testCheck_duplicate_spouse_and_marriage_date(self):
        self.assertFalse(check_duplicate_spouse_and_marriage_date() , "There is an a real doppleganger")
    def testCheck_duplicate_name_and_birth(self):
        self.assertFalse(check_duplicate_name_and_birth() , "There is an a real doppleganger")
    def testCheckMarriageBeforeDivorce(self):
        self.assertFalse(checkMarriageBeforeDivorce(), "There is a person married after their divorce")
    def testCheckMarriageBeforeDeath(self):
        self.assertFalse(checkMarriageBeforeDeath(), "There is a person married after their death")
    def testMultipleBirths(self):
        self.assertFalse(checkAllTuplets(), "There is a family with 6 or more children born at once")
    def testMaxSiblings(self):
        self.assertFalse(checkMaxSiblings(), "There is a family with 15 or more children")
    def testChildBeforeMarriageParent(self):
        self.assertFalse(childBeforeMarriageParent(), "There is a child born before marriage or after a divorce")
    def testChildBeforeDeathParent(self):
        self.assertFalse(childBeforeDeathParent(), "There is a child born before the death of their parent")
    def testSiblingGaps(self):
        self.assertFalse(checkAllTimesBetweenSiblings(), "There are siblings born less than 9 months apart that aren't twins")
    def testMaleLastNames(self):
        self.assertFalse(checkMaleLastNames(), "There is a male with a different last name than their family")

    def test_single_indivual(self):
        '''Test individual list with single Individual'''
        #create test indivual
        individual, all_individuals = self._create_individual_and_list()
        #test where there is only one individual
        error_msg = "Could not handle individual list with single entry"
        self.assertTrue(no_duplicate_name_and_birth(individual, all_individuals), error_msg)

    def test_no_duplicates(self):
        '''ensures the test is true with no duplicates'''
        individual, all_individuals = self._create_individual_and_list()


        completely_different_individual = Individual(1)
        completely_different_individual.name = "Joe Smith"
        completely_different_individual.birthday = "04 AUG 1968"
        all_individuals.append(completely_different_individual)
        error_msg = "No duplicate name and birthday. Main functionality broken"
        self.assertTrue(no_duplicate_name_and_birth(individual, all_individuals), error_msg)

    def test_two_duplicates(self):
        '''main functionality, test to detect a pair of duplicates'''
        individual, all_individuals = self._create_individual_and_list()

        duplicate_individual = Individual(2)
        duplicate_individual.name = "Alex Waldron"
        duplicate_individual.birthday = "01 JUL 2000"

        all_individuals.append(duplicate_individual)
        error_msg = "Could not detect duplicate individual when one was present"
        self.assertFalse(no_duplicate_name_and_birth(individual, all_individuals), error_msg)


    def test_multiple_duplicates(self):
        '''Test case with multiple duplicates '''
        individual, all_individuals = self._create_individual_and_list()

        duplicate_individual = Individual(2)
        duplicate_individual.name = "Alex Waldron"
        duplicate_individual.birthday = "01 JUL 2000"
        all_individuals.append(duplicate_individual)

        another_duplicate_individual = Individual(3)
        another_duplicate_individual.name = "Alex Waldron"
        another_duplicate_individual.birthday = "01 JUL 2000"
        all_individuals.append(another_duplicate_individual)

        error_msg = "Could not detect multiple duplicate individuals"
        self.assertFalse(no_duplicate_name_and_birth(individual, all_individuals), error_msg)

    def test_same_names(self):
        '''test individuals with the same name but different birthdays'''
        individual, all_individuals = self._create_individual_and_list()

        same_name_individual = Individual(4)
        same_name_individual.name = "Alex Waldron"
        same_name_individual.birthday = "04 AUG 1988"
        all_individuals.append(same_name_individual)

        error_msg = "detected duplicate when only names were the same not birthday"
        self.assertTrue(no_duplicate_name_and_birth(individual, all_individuals), error_msg)

    def test_correct_husb_role(self):
        individual, all_individuals = self._create_individual_and_list()
        newIndividual = Individual(5)
        newIndividual.name = "Alice"
        newIndividual.gender = 'F'
        individual.gender = "F"
        all_individuals.append(newIndividual)
        testFam = Family(0)
        testFam.wifeID = 0
        testFam.husbandID = 5 
        error_msg = "did not detect husband being female"
        self.assertFalse(correct_gender_for_role(testFam, all_individuals)["husbandMale"], error_msg)

    def test_correct_wife_role(self):
        individual, all_individuals = self._create_individual_and_list()
        newIndividual = Individual(5)
        newIndividual.name = "Alice"
        newIndividual.gender = 'M'
        individual.gender = "M"
        all_individuals.append(newIndividual)
        testFam = Family(0)
        testFam.wifeID = 0
        testFam.husbandID = 5 
        error_msg = "did not detect wife being male"
        self.assertFalse(correct_gender_for_role(testFam, all_individuals)["wifeFemale"], error_msg)

    def test_duplicate_fam_ids(self):
        fam1 = Family(0)
        fam2 = Family(0)

        error_msg = "did not detect duplicate family ids"
        self.assertFalse(check_unique_famID_indID([fam1,fam2],[Individual(0)])['uniqueFamIDs'], error_msg)

    def test_duplicate_ind_ids(self):
        ind1 = Individual(0)
        ind2 = Individual(0)

        error_msg = "did not detect duplicate individual ids"
        self.assertFalse(check_unique_famID_indID([Family(0)],[ind1,ind2])['uniqueIndIDs'], error_msg)

    def test_husband_wife_siblings(self):
      test_husb_id = "@I1@"
      test_wife_id = "@I2@"

      fam1 = Family(0)
      fam1.husbandID = test_husb_id
      fam1.wifeID = test_wife_id

      fam2 = Family(1)
      fam2.children = [test_husb_id, test_wife_id]

      families = [fam1,fam2]
      error_msg = "did not detect husband and wife being siblings"
      self.assertTrue(are_husb_wife_siblings(test_wife_id, test_husb_id, families), error_msg)

    def test_duplicate_child(self):
      child1_id = "@I2@"
      child2_id = "@I3@"

      child1 = Individual(child1_id)
      child1.name = "Alex Waldron"
      child1.birthday = "1 JUL 2000"

      child2 = Individual(child2_id)
      child2.name = "Alex Waldron"
      child2.birthday = "1 JUL 2000"

      individuals = [child1, child2]

      family = Family(0)
      family.children = [child1_id, child2_id]

      error_msg = "Did not detect two children with same first name and birthday"
      self.assertTrue(duplicate_children(family, individuals), error_msg)

      
    def test_no_marriage_to_descendants(self):
        fam1 = Family("@F1@")
        fam1.husbandID = "@I0@"
        fam1.wifeID = "@I1@"
        fam1.children = ["@I2@", "@I3@"]

        fam2 = Family("@F2@")
        fam2.husbandID = "@I0@"
        fam2.wifeID = "@I2@"

        families = [fam1, fam2]
        
        error_msg = "Did not detect father married to child"
        self.assertFalse(no_marriage_to_descendants(fam1, families), error_msg)

    def test_married_cousins(self):
        fam1 = Family("@F1@")
        fam1.husbandID = "@I0@"
        fam1.wifeID = "@I1@"
        fam1.children = ["@I2@", "@I3@"]

        fam1_1 =  Family("@F2@")
        fam1_1.husbandID = "@I2@" 
        fam1_1.children = ["@I4@"]

        fam1_2 = Family("@F2@")
        fam1_2.husbandID = "@I3@"
        fam1_2.children = ["@I5@"]

        fam1_1_1 = Family("@F3@")
        fam1_1_1.husbandID = "@I4@"
        fam1_1_1.wifeID = "@I5@"
        families = [fam1, fam1_1, fam1_2, fam1_1_1]

        error_msg = "Could not detect cousins were married"
        self.assertTrue(are_first_cousins_married(fam1, families), error_msg)

      

    def _create_individual_and_list(self):
        '''returns tuple of individual and list with single individual'''
        individual = Individual(0)
        individual.name = "Alex Waldron"
        individual.birthday = "01 JUL 2000"
        
        all_individuals = [individual]
        return (individual, all_individuals)

    

if __name__ == '__main__':
    #readfil()
    suite = unittest.TestLoader().loadTestsFromTestCase(Test)
    unittest.TextTestRunner().run(suite)
