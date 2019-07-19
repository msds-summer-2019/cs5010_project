"""

In Class Assignment 7: Testing Activity
Names: Aditi Rajagopal, Bradley Katcher, Charlie Putnam
Computing-ID: ar5vt, bk5pu, cmp2cz
Test Class - TestTheBookLovers
"""
from BookLover import *
import unittest

class TestTheBookLovers(unittest.TestCase): #inherits from unittest class
        
    def test_are_init_and_str_working(self):
        # initial test, correct number of mandatory parameters, print [] as books read
        user1 = BookLover('Aditi', 'artv5@virginia.edu', 'Humor')
        print("What's in booklovers? " + str(user1))
        self.assertEqual(str(user1), "Aditi has read []")

        # off by one test - didn't provide number of books, should print [] as books read
        user1 = BookLover('Aditi', 'artv5@virginia.edu', 'Humor', [('Merchant of Venice', 3), ('King Lear', 5), ('Pericles', 4)])
        self.assertEqual(str(user1), "Aditi has read []")

        # provide initial list of 3 books, should see them in the user object
        user1 = BookLover('Aditi', 'artv5@virginia.edu', 'Humor', 3, [('Merchant of Venice', 3), ('King Lear', 5), ('Pericles', 4)])
        print("What's in booklovers? " + str(user1))
        self.assertEqual(str(user1), "Aditi has read [('Merchant of Venice', 3), ('King Lear', 5), ('Pericles', 4)]")

        # have to provide name, email and favGenre - should get errors raised
        self.assertRaises(TypeError, lambda: BookLover('Aditi', 'artv5@virginia.edu'))
        self.assertRaises(TypeError, lambda: BookLover())

    def test_addBook_working(self):
        # no books read initially
        user1 = BookLover('Aditi', 'artv5@virginia.edu', 'Humor')
        self.assertEqual(str(user1), "Aditi has read []")

        # add one book
        user1.addBook('Merchant of Venice', 3)
        self.assertEqual(str(user1), "Aditi has read [['Merchant of Venice', 3]]")
        
        # add a few more
        user1.addBook('Pericles', 4)
        user1.addBook('Hamlet', 3)
        user1.addBook('12th Night', 5)
        user1.addBook('Romeo and Juliet', 1)
        self.assertEqual(str(user1), "Aditi has read [['Merchant of Venice', 3], ['Pericles', 4], ['Hamlet', 3], ['12th Night', 5], ['Romeo and Juliet', 1]]")
        
        # shouldn't add Pericles again
        user1.addBook('Pericles', 4)
        self.assertEqual(str(user1), "Aditi has read [['Merchant of Venice', 3], ['Pericles', 4], ['Hamlet', 3], ['12th Night', 5], ['Romeo and Juliet', 1]]")

    def test_hasRead_working(self):
        # not given books read initially - should return false
        user1 = BookLover('Aditi', 'artv5@virginia.edu', 'Humor')        
        self.assertEqual(user1.hasRead('King Lear'), False)

        # add one book, should say that you read it
        user1.addBook('Pericles', 4)
        self.assertEqual(user1.hasRead('Pericles'), True)

        # given an initial list of books read, verify that you haven't read all of them
        user2 = BookLover('Nathan', 'nwkarste@umich.edu', 'Sci-Fi', 2, [("Bad Omens", 4), ("Sandman", 5)])
        # not this one
        self.assertEqual(user2.hasRead('American Gods'), False)
        # but this one
        self.assertEqual(user2.hasRead('Sandman'), True)
        # and not this one
        self.assertEqual(user2.hasRead('The Sandman'), False)

    def test_numBooksRead_working(self):
        user1 = BookLover('Aditi', 'artv5@virginia.edu', 'Humor')
        self.assertEqual(user1.numBooksRead(), 0)
        user1.addBook('Pericles', 4)
        self.assertEqual(user1.numBooksRead(), 1)
        user2 = BookLover('Nathan', 'nwkarste@umich.edu', 'Sci-Fi', 2, [("Bad Omens", 4), ("Sandman", 5)])
        self.assertEqual(user2.numBooksRead(), 2)
        user1 = BookLover('Aditi', 'artv5@virginia.edu', 'Humor', 5)
        self.assertEqual(user1.numBooksRead(), 5)

    def test_favBooks_working(self):
        user1 = BookLover('Aditi', 'artv5@virginia.edu', 'Humor')
        user1.addBook('King Lear', 5)
        user1.addBook('Pericles', 4)
        user1.addBook('Hamlet', 3)
        user1.addBook('12th Night', 5)
        user1.addBook('Romeo and Juliet', 1)
        # shouldn't include Romeo and Juliet, or Hamlet
        self.assertEqual(user1.favBooks(), ['King Lear', 'Pericles', '12th Night'])
        # should include both books
        user2 = BookLover('Nathan', 'nwkarste@umich.edu', 'Sci-Fi', 2, [("Bad Omens", 4), ("Sandman", 5)])
        self.assertEqual(user2.favBooks(), ['Bad Omens', 'Sandman'])

if __name__ == '__main__':
    unittest.main()