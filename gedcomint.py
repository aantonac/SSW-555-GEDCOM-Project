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


def readfil():
    filename = "dataSet.ged"
    valid_tags = ["INDI", "NAME", "SEX", "BIRT", "DEAT", "FAMC","FAMS","FAM", "MARR", "HUSB", "WIFE", "CHIL", "DIV", "DATE", "HEAD", "TRLR", "NOTE"]

    with open(filename) as f:
        content = f.read().splitlines()
    d = Individual(0)
    indiv = []
    f = Family(0)
    fams = []
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
    printData(indiv, fams)
def findMonth(month):
    months = ["JAN", "FEB", "MAR","APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    for mon in months:
        if mon == month:
            return months.index(mon);
    return 0

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
        if individual.birthday != "":    
            birthdate = individual.birthday.split(" ")
            if(individual.alive):
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
