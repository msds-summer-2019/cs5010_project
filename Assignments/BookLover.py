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

    if bookLst:
      self.bookLst = bookLst
    else:
      self.bookLst = []
      
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