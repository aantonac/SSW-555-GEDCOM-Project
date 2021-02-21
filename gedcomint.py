'''
Created on Feb 12, 2021
@author: Steven Santiago
I pledge my Honor that I have abided by the Stevens Honor System.
'''
from prettytable import PrettyTable

class Individual:
    def __init__(self, id):
        self.id = id


class Family():
    def __init__(self, id):
        self.id = id


def readfil():
    filename = "dataSet.ged"
    valid_tags = ["INDI", "NAME", "SEX", "BIRT", "DEAT", "FAMC","FAMS","FAM", "MARR", "HUSB", "WIFE", "CHIL", "DIV", "DATE", "HEAD", "TRLR", "NOTE"]

    with open(filename) as f:
        content = f.read().splitlines()

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
                if i == 2:
                    t = s[6:-3]
                    s = s[0:6]
                    s+= x + "|Y|" + t
            elif i ==1 : 
                if x in valid_tags: 
                    s+= x + "|Y|"
                else:
                    s+= x + "|N|"
                i+=1
            else:
                s+=x + " "
        print(s)

def printData(individuals, families):
    ''' Receive list of Individual objects and Family objects as parameters, print
    and save output to output.txt'''
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

if __name__ == '__main__':
    readfil()

    individuals = [Individual(0)]
    families = [Family(0)]
    #pass individuals and families list as parameters to printData()
    printData(individuals, families)