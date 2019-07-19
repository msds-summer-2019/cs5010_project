"""

In Class Assignment 7: Testing Activity
Names: Aditi Rajagopal, Bradley Katcher, Charlie Putnam
Computing-ID: ar5vt, bk5pu, cmp2cz
Main Class - BookLovers
"""

class BookLover:
    
    #Initalize constructor with necessary attributes, making number of books and book list optional
    def __init__(self, name, email, favGenre, numBooks=None, bookLst=None):
        self.name = name
        self.email = email
        self.favGenre = favGenre
        
        #if a user provides numBooks arguement, take that value, if not, assign it to 0
        if numBooks:
            self.numBooks = numBooks
        else:
            self.numBooks = 0
        
        #if a user provides a book list, take that booklist, otherwise, initialize a blank one
        if bookLst:
            self.bookLst = bookLst
        else:
            self.bookLst = []
   
    #create a string constructor that prints out the user's name and the list of books they have read.
    def __str__(self):
        return (self.name + " has read " + str(self.bookLst))
    
    def addBook(self, bookName, rating):
        # add loop through books in book list, returning false if book is already in list
        for book in self.bookLst:
            if book[0] == bookName:
                return False
        # if book is not already in list, append it to the book list and increase the number of books and return true
        self.bookLst.append([bookName, rating])
        self.numBooks+=1
        
        return True
  
    def hasRead(self, bookName):
        # if book is in the booklist, return True, otherwise return false
        for book in self.bookLst:
            if book[0] == bookName:
                return True
            return False

    def numBooksRead(self): #return the number of books in the numBooks argument (initalized amount plus increases from addBook)
        return self.numBooks

    def favBooks(self):
        favBooks = [] #initalize an empty list
        for book in self.bookLst: #add only the book name (not rating) to favorite book list if the raiting is greater than 3
            if book[1] > 3:
                favBooks.append(book[0])
        return favBooks

#testing
user1 = BookLover('Aditi', 'artv5@virginia.edu', 'Humor')
user1.addBook('King Lear', 5)
user1.addBook('Pericles', 4)
user1.addBook('Hamlet', 3)
user1.addBook('12th Night', 5)
user1.addBook('Romeo and Juliet', 1)
print(user1.hasRead('King Lear'))
print(user1.hasRead('MacBeth'))
print(user1.numBooksRead())
print(user1.favBooks())
user1.addBook('King Lear', 5)
print(user1)

user2 = BookLover('Nathan', 'nwkarste@umich.edu', 'Sci-Fi', 2, [("Bad Omens", 4), ("Sandman", 5)])
print(user2)

