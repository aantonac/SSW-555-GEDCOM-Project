import unittest
from smellygedcomint import *

class TestDuplicates(unittest.TestCase):
    '''test cases for no_duplicate_name_and_birth which ensures there are no duplicate individuals in GEDCOM'''


    def test_single_indivual(self):
        '''Test individual list with single Individual'''
        #create test indivual
        individual, all_individuals = self.create_individual_and_list()
        #test where there is only one individual
        error_msg = "Could not handle individual list with single entry"
        self.assertTrue(no_duplicate_name_and_birth(individual, all_individuals), error_msg)

    def test_no_duplicates(self):
        '''ensures the test is true with no duplicates'''
        individual, all_individuals = self.create_individual_and_list()


        completely_different_individual = Individual(1)
        completely_different_individual.name = "Joe Smith"
        completely_different_individual.birthday = "04 AUG 1968"
        all_individuals.append(completely_different_individual)
        error_msg = "No duplicate name and birthday. Main functionality broken"
        self.assertTrue(no_duplicate_name_and_birth(individual, all_individuals), error_msg)

    def test_two_duplicates(self):
        '''main functionality, test to detect a pair of duplicates'''
        individual, all_individuals = self.create_individual_and_list()

        duplicate_individual = Individual(2)
        duplicate_individual.name = "Alex Waldron"
        duplicate_individual.birthday = "01 JUL 2000"

        all_individuals.append(duplicate_individual)
        error_msg = "Could not detect duplicate individual when one was present"
        self.assertFalse(no_duplicate_name_and_birth(individual, all_individuals), error_msg)


    def test_multiple_duplicates(self):
        '''Test case with multiple duplicates '''
        individual, all_individuals = self.create_individual_and_list()

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
        individual, all_individuals = self.create_individual_and_list()

        same_name_individual = Individual(4)
        same_name_individual.name = "Alex Waldron"
        same_name_individual.birthday = "04 AUG 1988"
        all_individuals.append(same_name_individual)

        error_msg = "detected duplicate when only names were the same not birthday"
        self.assertTrue(no_duplicate_name_and_birth(individual, all_individuals), error_msg)

    def create_individual_and_list(self):
        '''returns tuple of individual and list with single individual'''
        individual = Individual(0)
        individual.name = "Alex Waldron"
        individual.birthday = "01 JUL 2000"

        all_individuals = [individual]
        return (individual, all_individuals)


if __name__ == "__main__":
    unittest.main()