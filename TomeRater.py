# Tome Rater Capstone Project

# Joshua Le Gresley

# In this project I followed the instructions to create the User class, Book
# class, Fiction and NonFiction sub classes and TomeRater Class.
# I extended the project following the suggestions. I have added email
# verification, unique ISBN check and an evaluate method to give the user with
# most reviews. I have also added a method to give a user a random
# recommendation depending on a users preference of Fiction or Non fiction
# books.

# Following on from this I have attempted to create a simple programme
# (line386) to allow user input flow through the functionality of the created
# classes. In This I have also added a method to allow the user to delete a
# book from their catalogue


import re
import random
# Create a user class


class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, new_email):
        self.email == new_email
        return f"Your email has been updated to {new_email}"

    def __repr__(self):
        return f"User: {self.name}, email: {self.email}, Books read: {len(self.books)}"""

    def __eq__(self, other_user):
        return self.name == other_user.name or self.email == other_user.email

    def read_book(self, book, rating=None):
        new_read_book = self.books[book] = rating
        return new_read_book

    def del_read_book(self, book):
        rating = self.books.pop(book)
        book.del_rating(rating)
        return f"\nThe book {book} has been deleted from your catalogue"

    def get_average_rating(self):
        count = 0
        total = 0
        try:
            for rating in self.books.values():
                if isinstance(rating, int):
                    count += rating
                    total += 1
                else:
                    continue
            return count/total
        except ZeroDivisionError:
            return 0


# Create book class


class Book(object):
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, new_isbn):
        self.isbn == new_isbn
        return f"{self.title}'s ISBN has been updated to {new_isbn}"

    def add_rating(self, rating):
        try:
            if 0 <= rating <= 4:
                self.ratings.append(rating)
                return rating
        except TypeError:
            self.ratings.append(None)
        except ValueError:
            return "Invalid Rating! Please try again"

    def del_rating(self, rating):
        try:
            if 0 <= rating <= 4:
                self.ratings.remove(rating)
                return rating
        except TypeError:
            self.ratings.remove(None)
        except ValueError:
            return "Invalid Rating! Please try again"

    def __eq__(self, other_book):
        return self.title == other_book.title and self.isbn == other_book.isbn

    def get_average_rating(self):
        count = 0
        total = 0
        try:
            for rating in self.ratings:
                if isinstance(rating, int):
                    count += rating
                    total += 1
                else:
                    continue
            return count/total
        except ZeroDivisionError:
            return 0

    def __repr__(self):
        return f"{self.title}"

    def __hash__(self):
        return hash((self.title, self.isbn))


# Fiction subclass of Book subclass


class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return f"{self.title} by {self.author}"


# NON-Fiction subclass of Book class

class NonFiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return f"{self.title}, {self.level} level book on {self.subject}"

# Create TomeRater subclass


class TomeRater(object):
    def __init__(self):
        self.users = {}
        self.books = {}

    def check_isbn(self, new_isbn):
        for book in self.books.keys():
            if book.get_isbn() == new_isbn:
                raise ValueError
        if len(str(new_isbn)) == 10 or len(str(new_isbn)) == 13:
            return "This is a valid ISBN"
        else:
            raise ValueError

    def create_book(self, title, isbn):
        new_book = Book(title, isbn)
        return new_book

    def create_novel(self, title, author, isbn):
        new_novel = Fiction(title, author, isbn)
        return new_novel

    def create_non_fiction(self, title, subject, level, isbn):
        new_non_fiction = NonFiction(title, subject, level, isbn)
        return new_non_fiction

    def add_book_to_user(self, book, email, rating=None):
        if email in self.users.keys():
            for book_ in self.users[email].books.keys():
                if book == book_:
                    return '\nBook title or ISBN already exists. Please try again\n'
            self.users[email].read_book(book, rating)
            book.add_rating(rating)
            for book_ in self.books.keys():
                if book_ == book:
                    self.books[book_] = self.books[book_] + 1
                    return book
            self.books[book] = 1
            return book
        else:
            return f"\nNo user with email: {email}\n"

    def email_verification(self, email):
        match = re.match(
            '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
        if match is None:
            raise ValueError

    def change_email(self, email, new_email):
        self.email_verification(new_email)
        user_obj = self.users.pop(email)
        self.users[new_email] = user_obj
        return f"\nYour registered email has been updated to {new_email}"

    def add_user(self, name, email, user_books=None):
        try:
            self.email_verification(email)
        except ValueError:
            return "Invalid email. Please try again"
        new_user = User(name, email)
        for user in self.users.values():
            if new_user == user:
                return "\nUser name or email already exists. Please try again\n"
        self.users[email] = new_user
        if not user_books:
            return new_user
        else:
            for book in user_books:
                self.add_book_to_user(book, email, rating=None)
            return new_user

    def del_book_from_user(self, email, book):
        if email in self.users.keys():
            self.users[email].del_read_book(book)
            if self.books[book] < 2:
                self.books.pop(book)
                return f"{book} has been altered or deleted"
            else:
                self.books[book] = self.books[book] - 1
                return f"{book} has been altered or deleted"
        else:
            return f"\nNo user with email: {email}!\n"

    def print_catalog(self):
        catalogue = []
        for book in self.books.keys():
            catalogue.append(book)
        return catalogue

    def print_users(self):
        users = []
        for user in self.users.values():
            users.append(user)
        return users

    def __repr__(self):
        return f"""
Tome Rater's current users include:
        {self.print_users()}
Tome Rater's current book catalogue includes:
        {self.print_catalog()}"""

    def get_most_read_book(self):
        most_read = 0
        books = []
        for book, reads in self.books.items():
            if reads > most_read:
                most_read = reads
                books[:] = []
                books.append(book.get_title())
            elif reads == most_read:
                books.append(book.get_title())
        for book in books:
            print(f"{book} has been read {most_read} times")

    def highest_rated_book(self):
        highest_rating = 0
        highest_rated_book = []
        for book in self.books.keys():
            average_rating = book.get_average_rating()
            if average_rating > highest_rating:
                highest_rating = average_rating
                highest_rated_book[:] = []
                highest_rated_book.append(book.get_title())
            elif average_rating == highest_rating:
                highest_rated_book.append(book.get_title())
        for book in highest_rated_book:
            print(f"{book} has an average rating of {format(highest_rating, '.2f')}")

    def most_positive_user(self):
        highest_average = 0
        most_positive = []
        for user in self.users.values():
            average_rating = user.get_average_rating()
            if average_rating > highest_average:
                highest_average = average_rating
                most_positive[:] = []
                most_positive.append(user.name)
            elif average_rating == highest_average:
                most_positive.append(user.name)
        for user in most_positive:
            print(f"{user} gives an average rating of {format(highest_average, '.2f')}")

    def most_reviews(self):
        books_read = 0
        users = []
        for email, user in self.users.items():
            if len(self.users[email].books) > books_read:
                books_read = len(Tome_Rater.users[email].books)
                users[:] = []
                users.append(user.name)
            elif len(self.users[email].books) == books_read:
                users.append(user.name)
        for user in users:
            print(
                f"{user} with {books_read} reviews uploaded. \nKeep up the good work")

    def recomendation(self, email):
        non_fiction = [book for book in self.users[email].books.keys() if type(book) == NonFiction]
        fiction = [book for book in self.users[email].books.keys() if type(book) == Fiction]
        if len(non_fiction) > len(fiction):
            non_fic_cata = [book for book in self.books.keys() if type(book) == NonFiction]
            print(f"""-*-*-*-Daily Recommendation-*-*-*-
        We see that you read more Non Fiction books. Have you tried {random.choice(non_fic_cata)}
            """)
        else:
            fic_cata = [book for book in self.books.keys() if type(book) == Fiction]
            print(f"""-*-*-*-Daily Recommendation-*-*-*-
        We see that you read more Fiction books. Have you tried {random.choice(fic_cata)}
            """)


# Populate.py
# Books and users Test
# Some books ISBN's have been altered from the original populate.py file to
# meet the requirements I have defined, of correct 10 or 13 digit ISBN number.

Tome_Rater = TomeRater()

# Create some books:
book1 = Tome_Rater.create_book("Society of Mind", 1234567888)
novel1 = Tome_Rater.create_novel("Alice In Wonderland", "Lewis Carroll", 1888882345)
novel1.set_isbn(9781536831139)
nonfiction1 = Tome_Rater.create_non_fiction(
    "Automate the Boring Stuff", "Python", "beginner", 1929452000)
nonfiction2 = Tome_Rater.create_non_fiction(
    "Computing Machinery and Intelligence", "AI", "advanced", 1111193800)
novel2 = Tome_Rater.create_novel("The Diamond Age", "Neal Stephenson", 1010101000)
novel3 = Tome_Rater.create_novel("There Will Come Soft Rains", "Ray Bradbury", 1000100000)

# Create users:
Tome_Rater.add_user("Alan Turing", "alan@turing.com")
Tome_Rater.add_user("David Marr", "david@computation.org")

# Add a user with three books already read:
Tome_Rater.add_user("Marvin Minsky", "marvin@mit.edu", user_books=[book1, novel1, nonfiction1])

# Add books to a user one by one, with ratings:
Tome_Rater.add_book_to_user(book1, "alan@turing.com", 1)
Tome_Rater.add_book_to_user(novel1, "alan@turing.com", 3)
Tome_Rater.add_book_to_user(nonfiction1, "alan@turing.com", 3)
Tome_Rater.add_book_to_user(nonfiction2, "alan@turing.com", 4)
Tome_Rater.add_book_to_user(novel3, "alan@turing.com", 1)

Tome_Rater.add_book_to_user(novel2, "marvin@mit.edu", 2)
Tome_Rater.add_book_to_user(novel3, "marvin@mit.edu", 2)
Tome_Rater.add_book_to_user(novel3, "david@computation.org", 4)

# Uncomment these to test your functions:
print("\nBooks in catalogue:\n")
for book in Tome_Rater.print_catalog():
    print(book)
print("\nUsers in TomeRater:\n")
for user in Tome_Rater.print_users():
    print(user)

print("\nMost positive user:")
Tome_Rater.most_positive_user()
print("\nHighest rated book:")
Tome_Rater.highest_rated_book()
print("\nMost read book:")
Tome_Rater.get_most_read_book()


# TomeRater User Input Programme.

# In an extension to the project I have atempted to create a simple programme
# to allow user input in the classes create in the capstone project.


def tome_rater_menu():
    print("""
|----Welcome to Tome Rater!----|

     This is this place to come if you love Books!
     In this program you have the chance to rate the books any book you read.
     And share your scores with all your friends.

     We'll also help you along the way with a daily recommendation of a book
     you might enjoy!

      """)
    print("Are you an existing User?\n")
    response = str(
        input("If yes please enter your registered email \nIf your new here please press # to register >>>"))
    if response in Tome_Rater.users.keys():
        existing_user(response)
    elif response == "#":
        new_user()
    else:
        print("\nThis email is not recognised, please try again!")
        tome_rater_menu()


def existing_user(email):
    print("""
|---Welcome to Tome Rater!---|

Your existing books and ratings include:
""")
    if not Tome_Rater.users[email].books:
        print("You have no books currently available\n")
    else:
        for book, rating in Tome_Rater.users[email].books.items():
            print(f"{book} has a rating of {rating}.")
    print("\n")
    if not Tome_Rater.books:
        print("\nNo books currently in catalogue")
    else:
        Tome_Rater.recomendation(email)
    print("""
What would you like to do today?
Please select from the options below:
    1. Add a new book
    2. Delete an existing book
    3. Add a rating to an existing book
    4. View a list of our entire catalogue
We also have a range of options to update details related to your books or your account:
    5. Change a books ISBN number
    6. Change your registered email address

Or we can help you analysise your favourite books:
    7. Get your cumulative average book rating
    8. Get any books average rating from our catalogue
    9. Find out the Author of a novel in our catalogue
    10. Find out the recomended level of any Non Fiction in our catalogue
    11. Find out the most read book in our catalogue
    12. Find out the highest rated book in our catalogue
    13. Find out the most positive user on Tome Rater
    14. Find out who Tome Rater's most avid reviewer is.
    """)
    try:
        response = int(input(
            "Please select a number between 1 and 12 to select an option \nAlternatively press 0 to logout >>>"))
        if response == 0:
            print("\nAre you sure you want to end this session\n")
            response = str(input("Please press y to logout or n to see your options again >>>"))
            if response == 'y':
                tome_rater_menu()
            elif response == 'n':
                existing_user(email)
            else:
                print("This was an invalid input, please try again!")
                existing_user(email)
        elif response == 1:
            add_individual_book(email)
        elif response == 2:
            delete_book(email)
        elif response == 3:
            add_rating_to_book(email)
        elif response == 4:
            view_catalogue(email)
        elif response == 5:
            change_isbn(email)
        elif response == 6:
            change_email(email)
        elif response == 7:
            user_average(email)
        elif response == 8:
            book_average(email)
        elif response == 9:
            author(email)
        elif response == 10:
            difficulty(email)
        elif response == 11:
            most_read(email)
        elif response == 12:
            highest_rated(email)
        elif response == 13:
            positive_user(email)
        elif response == 14:
            most_prolific_reader(email)
        else:
            print("\nThis was an invalid input, please try again!")
            existing_user(email)
    except ValueError:
        print("\nThis was an invalid input, please try again!")
        existing_user(email)


def new_user():
    print("""
Welcome new member to Tome Rater!
Thankyou for choosing our book review platform.
""")
    name = name_input()
    email = email_input()
    new_user_add = Tome_Rater.add_user(name, email)
    if type(new_user_add) is User:
        print("\nWould you like to add books to your catalogue now?\n")
        response = str(input("Please enter y for yes or n for no >>>"))
        if response == 'n':
            pass
        elif response == 'y':
            user_books = create_user_book(email)
    else:
        print(f"\n{new_user_add}\n")
        tome_rater_menu()
    print(f"""
    Your new profile has been created!
        Your registered name is {name}
        Your registered email is {email}
        """)
    existing_user(email)


def name_input():
    name = str(input("Please enter your full name >>>")).title()
    print(f"\nYou entered {name}. \nIs this the name you'd like to add?\n")
    response = str(input("Please enter y for yes or n for no >>>"))
    if response == 'n':
        new_user()
    elif response == 'y':
        return name
    else:
        print("\nThis was an invalid input, please try again!\n")
        new_user()


def email_input():
    email = str(input("\nPlease enter your email address >>>"))
    print(f"\nYou entered {email}. \nIs this the email you'd like to add?\n")
    response = str(input("Please enter y for yes or n for no >>>"))
    if response == 'n':
        new_user()
    elif response == 'y':
        return email
    else:
        print("\nThis was an invalid input, please try again!\n")
        new_user()


def create_user_book(email, book_lst=[]):
    first_books = book_lst
    book_title = input_title(email, first_books)
    if book_title == []:
        return first_books
    else:
        try:
            book_isbn = input_isbn(email, first_books)
            Tome_Rater.check_isbn(book_isbn)
        except ValueError:
            print("Invalid ISBN. Please enter a UNIQUE 10 or 13 digit ISBN number")
            create_user_book(email, first_books)
        else:
            print("\nIs this book fiction or non-fiction?\n")
        try:
            response = int(input("Please enter 1 for fiction, or 2 for non-fiction >>>"))
            if response == 1:
                book_author = input_fiction(email, first_books)
                if book_author == '#':
                    book = Tome_Rater.create_book(book_title, book_isbn)
                    first_books.append(book)
                else:
                    novel = Tome_Rater.create_novel(book_title, book_author, book_isbn)
                    first_books.append(novel)
            elif response == 2:
                book_subject = input_book_subject(email, first_books)
                book_level = input_book_level(email, first_books)
                non_fic = Tome_Rater.create_non_fiction(
                    book_title, book_subject, book_level, book_isbn)
                first_books.append(non_fic)
            else:
                print("\nThis was an invalid input, please try again!\n")
                create_user_book(email, first_books)
        except ValueError:
            print("This was an invalid input, please try again!")
            create_user_book(email, first_books)
        print("\nWould you like to enter another book?\n")
        response2 = str(input("Please enter y for yes or n for no >>>"))
        if response2 == 'y':
            create_user_book(email, first_books)
        elif response2 == 'n':
            add_ratings(email, first_books)
        else:
            print("\nThis was an invalid input, please try again!")
            create_user_book(email, first_books)


def input_title(email, book_lst=[]):
    book_title = str(input("\nPlease enter the title of a book or enter # to skip >>>")).title()
    if book_title == '#':
        return []
    else:
        print(f"\nYou entered {book_title}. \nIs this the book you'd like to add?\n")
        response = str(input("Please enter y for yes or n for no >>>"))
        if response == 'n':
            create_user_book(email, book_lst)
        elif response == 'y':
            return book_title
        else:
            print("\nThis was an invalid input, please try again!\n")
            create_user_book(email, book_lst)


def input_isbn(email, book_lst=[]):
    try:
        isbn = int(input("\nPlease enter an ISBN number >>>"))
        print(f"\nYou entered {isbn}. \nIs this the ISBN you'd like to add?\n")
        response = str(input("Please enter y for yes or n for no >>>"))
        if response == 'n':
            input_isbn(email, book_lst)
        elif response == 'y':
            return isbn
        else:
            print("\nThis was an invalid input, please try again!\n")
            input_isbn(email, book_lst)
    except ValueError:
        print("\nThis was an invalid input, please try again!\n")
        input_isbn(email, book_lst)


def input_fiction(email, book_lst=[]):
    author = str(input("\nPlease enter the author of the book or enter # to skip >>>")).title()
    if author == '#':
        return '#'
    else:
        print(f"\nYou entered {author}. \nIs this the Author you'd like to add?\n")
        response = str(input("Please enter y for yes or n for no >>>"))
        if response == 'n':
            create_user_book(email, book_lst)
        elif response == 'y':
            return author
        else:
            print("\nThis was an invalid input, please try again!\n")
            create_user_book(email, book_lst)


def input_book_subject(email, book_lst=[]):
    book_subject = str(input("\nPlease enter the subject of this book >>>")).title()
    print(f"\nYou entered {book_subject}. \nIs this the Subject you'd like to add?\n")
    response = str(input("Please enter y for yes or n for no >>>"))
    if response == 'n':
        create_user_book(email, book_lst)
    elif response == 'y':
        return book_subject
    else:
        print("\nThis was an invalid input, please try again!\n")
        create_user_book(email, book_lst)


def input_book_level(email, book_lst=[]):
    book_level = str(input("\nPlease enter the level of the book >>>")).title()
    print(f"\nYou entered {book_level}. \nIs this the level you'd like to add?\n")
    response = str(input("Please enter y for yes or n for no >>>"))
    if response == 'n':
        create_user_book(email, book_lst)
    elif response == 'y':
        return book_level
    else:
        print("\nThis was an invalid input, please try again!\n")
        create_user_book(email, book_lst)


def add_individual_book(email):
    books = []
    book_lst = create_user_book(email, books)
    if book_lst == []:
        print("\nPlease try again\n")
        existing_user(email)
    else:
        add_individual_book(email)


def add_ratings(email, books=[]):
    try:
        for book in books:
            rating = int(
                input(f"\nPlease enter a rating for {book} between 0 and 4 or enter 5 to skip rating >>>"))
            if rating == 5:
                new_book = Tome_Rater.add_book_to_user(book, email)
                if type(new_book) is Book:
                    print(f"\nThe book {book} has been added to your book list")
                else:
                    print(f"\n{new_book}")
            elif 0 <= rating <= 4:
                rated_new_book = Tome_Rater.add_book_to_user(book, email, rating)
                if type(rated_new_book) is Book:
                    print(
                        f"\nThe book {book} with a rating of {rating} has been added to your book list")
                else:
                    print(f"\n{rated_new_book}")
            else:
                print("\nThis was an invalid input, please try again!\n")
                add_ratings(email, books=[])
        existing_user(email)
    except ValueError:
        print("\nThis was an invalid input, please try again!\n")
        add_ratings(email, books=[])


def add_rating_to_book(email):
    if not Tome_Rater.users[email].books:
        print("\nNo books currently in catalogue")
        existing_user(email)
    else:
        book = []
        print("\nPlease enter which book's rating you would like to update\n")
        selection = user_catalogue_selection(email)
        book.append(selection)
        Tome_Rater.del_book_from_user(email, selection)
        add_ratings(email, book)


def view_catalogue(email):
    if not Tome_Rater.books:
        print("\nNo books currently in catalogue")
        existing_user(email)
    else:
        catalogue = Tome_Rater.print_catalog()
        print("\nOur full catalogue includes the following titles: \n")
        for book in catalogue:
            print(f"--{book}")
        existing_user(email)


def change_isbn(email):
    if not Tome_Rater.users[email].books:
        print("\nNo books currently in catalogue")
        existing_user(email)
    else:
        print("\nPlease enter which book's ISBN you would like to update\n")
        book_obj = user_catalogue_selection(email)
        print(f"\nThe ISBN is currently {book_obj.get_isbn()}\n")
        new_isbn = input_isbn(email)
        try:
            Tome_Rater.check_isbn(new_isbn)
        except ValueError:
            print("Invalid ISBN. Please enter a UNIQUE 10 or 13 digit ISBN number")
            change_isbn(email)
        else:
            if type(book_obj) is Fiction:
                new_book = Tome_Rater.create_novel(book_obj.title, book_obj.author, new_isbn)
            elif type(book_obj) is NonFiction:
                new_book = Tome_Rater.create_non_fiction(
                    book_obj.title,  book_obj.subject, book_obj.level, new_isbn)
            else:
                new_book = Tome_Rater.create_book(book_obj.title, new_isbn)
            new_book.set_isbn(new_isbn)
            rating = Tome_Rater.users[email].books[book_obj]
            Tome_Rater.del_book_from_user(email, book_obj)
            Tome_Rater.add_book_to_user(new_book, email, rating)
            print(f"\n{new_book.title}'s ISBN has been updated to {new_isbn}\n")
            existing_user(email)


def change_email(email):
    print(f"\nYour current registered email is: \n\t{email}\n")
    new_email = str(input("\nPlease enter your new email >>>"))
    print(f"\nYou entered {new_email}. \nIs this the email you'd like to add?\n")
    response = str(input("Please enter y for yes or n for no >>>"))
    if response == 'y':
        try:
            new = Tome_Rater.change_email(email, new_email)
        except ValueError:
            print("\nInvaild email. Please try again\n")
            existing_user(email)
        else:
            print(f"{new}\n")
            existing_user(new_email)
    elif response == 'n':
        existing_user(email)
    else:
        print("\nThis was an invalid input, please try again!\n")
        existing_user(email)


def user_average(email):
    print(
        f"\nYour current average rating: \n\t{format(Tome_Rater.users[email].get_average_rating(), '.2f')}")
    existing_user(email)


def book_average(email):
    if not Tome_Rater.books:
        print("\nNo books currently in catalogue")
        existing_user(email)
    else:
        print("\nPlease enter which book you would like the average rating of\n")
        selection = catalogue_selection(email)
        print(f"\n{selection}'s average rating is {format(selection.get_average_rating(), '.2f')}\n")
        existing_user(email)


def author(email):
    if not Tome_Rater.books:
        print("\nNo books currently in catalogue")
        existing_user(email)
    else:
        print("\nPlease enter which Fiction book you would like to find the author\n")
        selection = catalogue_selection(email, Fiction)
        print(f"\n{selection.title}'s aurthor is {selection.get_author()}\n")
        existing_user(email)


def difficulty(email):
    if not Tome_Rater.books:
        print("\nNo books currently in catalogue")
        existing_user(email)
    else:
        print("\nPlease enter which Non Fiction book you would like to find the level\n")
        selection = catalogue_selection(email, NonFiction)
        print(f"\n{selection.title}'s level is {selection.get_level()}\n")
        existing_user(email)


def most_read(email):
    if not Tome_Rater.books:
        print("\nNo books currently in catalogue")
        existing_user(email)
    else:
        print("\nThe most read book/books in our catalogue:\n")
        Tome_Rater.get_most_read_book()
        existing_user(email)


def highest_rated(email):
    if not Tome_Rater.books:
        print("\nNo books currently in catalogue")
        existing_user(email)
    else:
        print("\nThe highest rated book/books in our catalogue:\n")
        Tome_Rater.highest_rated_book()
        existing_user(email)


def positive_user(email):
    print("\nThe most positive user/users:\n")
    Tome_Rater.most_positive_user()
    existing_user(email)


def most_prolific_reader(email):
    print("\n The most avid reviewer/s:")
    Tome_Rater.most_reviews()
    existing_user(email)


def delete_book(email):
    if not Tome_Rater.users[email].books:
        print("\nNo books currently in catalogue")
        existing_user(email)
    else:
        print("Please enter which book you would like to delete from your catalogue")
        book_obj = user_catalogue_selection(email)
        deleted = Tome_Rater.del_book_from_user(email, book_obj)
        print(f"\n{deleted}")
        existing_user(email)


def user_catalogue_selection(email, book_type=None):
    count_ = 0
    books_ = {}
    if book_type is Fiction:
        for book in Tome_Rater.users[email].books.keys():
            if type(book) is Fiction:
                count_ += 1
                books_[count_] = book
                print(f"{count_}. {book.title}")
    elif book_type is NonFiction:
        for book in Tome_Rater.users[email].books.keys():
            if type(book) is NonFiction:
                count_ += 1
                books_[count_] = book
                print(f"{count_}. {book.title}")
    else:
        for book in Tome_Rater.users[email].books.keys():
            count_ += 1
            books_[count_] = book
            print(f"{count_}. {book.title}")
    try:
        response = int(input(f"Please enter 1 to {len(books_)} >>>"))
        if 1 <= response <= len(books_):
            for count, book in books_.items():
                if count == response:
                    return book
        else:
            print("\nThis was an invalid input, please try again!")
            existing_user(email)
    except ValueError:
        print("\nThis was an invalid input, please try again!")
        existing_user(email)


def catalogue_selection(email, book_type=None):
    count_ = 0
    books_ = {}
    if book_type is Fiction:
        for book in Tome_Rater.print_catalog():
            if type(book) is Fiction:
                count_ += 1
                books_[count_] = book
                print(f"{count_}. {book.title}")
    elif book_type is NonFiction:
        for book in Tome_Rater.print_catalog():
            if type(book) is NonFiction:
                count_ += 1
                books_[count_] = book
                print(f"{count_}. {book.title}")
    else:
        for book in Tome_Rater.print_catalog():
            count_ += 1
            books_[count_] = book
            print(f"{count_}. {book.title}")
    try:
        response = int(input(f"Please enter 1 to {len(books_)} >>>"))
        if 1 <= response <= len(books_):
            for count, book in books_.items():
                if count == response:
                    return book
        else:
            print("\nThis was an invalid input, please try again!")
            existing_user(email)
    except ValueError:
        print("\nThis was an invalid input, please try again!")
        existing_user(email)


tome_rater_menu()
