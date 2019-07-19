#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 14:52:45 2019

@author: Bradley
"""

"""

In Class Assignment 7: Testing Activity
Names: Aditi Rajagopal, Bradley Katcher, Charlie Putnam
Computing-ID: ar5vt, bk5pu, cmp2cz
Main Class - BookLovers
"""

class BookLoverErrors:
    
    #Initalize constructor with necessary attributes, making number of books and book list optional
    def __init__(self, name, email, favGenre, numBooks=None, bookLst=None):
        self.name = name
        self.email = email
        self.favGenre = favGenre
        
        #if a user provides numBooks arguement, take that value, if not, assign it to 0
        if numBooks:
            self.numBooks = numBooks
        else:
            self.numBooks = 1 #initalize the number of books read at one even if none are provided (Error 1) 
        
        #if a user provides a book list, take that booklist, otherwise, initialize a blank one
        if bookLst:
            self.bookLst = bookLst
        else:
            self.bookLst = []
   
    #create a string constructor that prints out the user's name and the list of books they have read.
    def __str__(self):
        return ''
       # return (self.name + " has read " + str(self.bookLst)) Nothing is returned when the string is called upon (Error 7)
    
    def addBook(self, bookName, rating):
        # add loop through books in book list, returning false if book is already in list
        # add books regardless of whether they are already in list (Error 2) 
#        for book in self.bookLst:
#            if book[0] == bookName:
#                return False
        # if book is not already in list, append it to the book list and increase the number of books and return true
        self.bookLst.append([bookName, rating])
        self.numBooks+=3 # adds three books to number of books every time one is added (Error 3)
        
        return True
  
    def hasRead(self, bookName):
        # if book is in the booklist, return True, otherwise return false
        for book in self.bookLst:
            if book[0] == bookName:
                return True
            return True #returns Trie no matter what (Error 4)

    def numBooksRead(self): #return the number of books in the numBooks argument (initalized amount plus increases from addBook)
        return self.numBooks

    def favBooks(self):
        favBooks = [] #initalize an empty list
        for book in self.bookLst: #add only the book name (not rating) to favorite book list if the raiting is greater than 3
            if book[1] >= 3:  #greater than or equal to three when it should be three (Error 5)
                favBooks.append(book[1]) # returns raitings of books not book names (Error 6)
        return favBooks


