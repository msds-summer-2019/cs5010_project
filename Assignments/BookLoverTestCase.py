# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 13:31:12 2019

@author: cmp2c
"""

import unittest
from BookLover import *


class BookLoverTestCase(unittest.TestCase): # inherit from unittest.TestCase
    
    #Test that the length of bookLst equals the number of books
    def test_init_num_books_equals_bookLst_len(self):
       
        #setup
        b1 = BookLover('Aditi', 'artv5@virginia.edu', 'Humor', 1, [('Catcher in the Rye',1),("Ender's Game", 5)] )# create instance
        bookLstLen = len([x[0] for x in b1.bookLst])
        
        # Test that the length of bookLst equals the number of books
        self.assertEqual(b1.numBooks, bookLstLen)
    
    def testAddBook_no_dupes(self):
        
        #setup
        b1 = BookLover('Charlie', 'cmp2cz@virginia.edu', 'Sci-Fi', 1, [('Catcher in the Rye',1),("Ender's Game", 5)] )# create instance
        result = b1.addBook("Ender's Game", 1)
        
        self.assertFalse(result)
        
    def testAddBook(self):
        #setup
        b1 = BookLover('Charlie', 'cmp2cz@virginia.edu', 'Sci-Fi', 1, [('Catcher in the Rye',1),("Ender's Game", 5)] )# create instance
        result = b1.addBook("The Notebook", 5)
        
        self.assertTrue(result)
        
    def testAddBook_increment_numBooks(self):
        
        b1 = BookLover('Charlie', 'cmp2cz@virginia.edu', 'Sci-Fi', 1, [('Catcher in the Rye',1),("Ender's Game", 5)] )# create instance
        result = b1.addBook("The Notebook", 5)
        
        self.assertEqual(b1.numBooks, 3)
        
    def testHasReadTrue(self):
        #setup
        b1 = BookLover('Charlie', 'cmp2cz@virginia.edu', 'Sci-Fi', 1, [('Catcher in the Rye',1),("Ender's Game", 5)] )# create instance
        result = b1.hasRead("Ender's Game")
        
        self.assertTrue(result)
        
    def testHadReadFalse(self):
        #setup
        b1 = BookLover('Charlie', 'cmp2cz@virginia.edu', 'Sci-Fi', 1, [('Catcher in the Rye',1),("Ender's Game", 5)] )# create instance
        result = b1.hasRead("The Notebook")
        
        self.assertFalse(result)
        
    def testEqualsNumBooksRead(self):
        #set up
        b1 = BookLover('Charlie', 'cmp2cz@virginia.edu', 'Sci-Fi', 1, [('Catcher in the Rye',1),("Ender's Game", 5)] )# create instance

        #get number of books from bookLst
        bookLstLen = len([x[0] for x in b1.bookLst])
        #get result from numBooksRead
        result = b1.numBooksRead()
        #compare results
        self.assertEqual(bookLstLen, result)
        
        
    def testNumBooksRead_nobooks(self):
        
        #set up, but without passing any books
        b1 = BookLover('Charlie', 'cmp2cz@virginia.edu', 'Sci-Fi')# create instance

        #get number of books from bookLst (add one to )
        bookLstLen = len([x[0] for x in b1.bookLst])
        #get result from numBooksRead
        result = b1.numBooksRead()
        #compare results (should not be equal)
        self.assertEqual(bookLstLen, result)
        
    def testFavBooksCorrect(self):
        
        b1 = BookLover('Charlie', 'cmp2cz@virginia.edu', 'Sci-Fi', 1, [('Catcher in the Rye',1),("Ender's Game", 5)] )# create instance
        favBookExpectation = []
        for book in b1.bookLst:
            if book[1] > 3:
                favBookExpectation.append(book[0])
        print(favBookExpectation)
        
        result = b1.favBooks()
        
        self.assertEqual(favBookExpectation, result)
        
    def testFavBooksIncorrectInequality(self):
        
        b1 = BookLover('Charlie', 'cmp2cz@virginia.edu', 'Sci-Fi', 1, [('Catcher in the Rye',1),("Ender's Game", 3)] )# create instance
        favBookExpectation = []
        for book in b1.bookLst:
            #change the inequality to 3 or greater
            if book[1] >= 3:
                favBookExpectation.append(book[0])
        print(favBookExpectation)
        
        result = b1.favBooks()
        
        print(result)
        
        self.assertNotEqual(favBookExpectation, result)

                
if __name__ == '__main__':
    unittest.main()            