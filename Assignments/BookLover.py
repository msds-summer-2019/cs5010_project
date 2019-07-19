"""

In Class Assignment 7: Testing Activity
Names: Aditi Rajagopal, Bradley Katcher, Charlie Putnam
Computing-ID: ar5vt, bk5pu, cmp2cz
Main Class - BookLovers
"""

class BookLover:
  def __init__(self, name, email, favGenre, numBooks=None, bookLst=None):
    self.name = name
    self.email = email
    self.favGenre = favGenre
    
    if numBooks:    
        self.numBooks = numBooks
    else:
        self.numBooks = 0

    if bookLst and numBooks:
      self.bookLst = bookLst
      self.numBooks = len([x[0] for x in bookLst])
    else:
      self.bookLst = []
      self.numBooks = 0
      
  def __str__(self):
    return (self.name + " has read " + str(self.bookLst))

  def addBook(self, bookName, rating):
    for book in self.bookLst:
      if book[0] == bookName:
        return False
    self.bookLst.append([bookName, rating])
    self.numBooks+=1
    return True

  def hasRead(self, bookName):
    for book in self.bookLst:
      if book[0] == bookName:
        return True
    return False

  def numBooksRead(self):
    return self.numBooks

  def favBooks(self):
    favBooks = []
    for book in self.bookLst:
      if book[1] > 3:
        favBooks.append(book[0])
    return favBooks

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

