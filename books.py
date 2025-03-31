#hi
from datetime import datetime
import sqlite3

connection = sqlite3.connect("Library.sl3")
cur = connection.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    author TEXT,
    year_published INTEGER,
    copies INTEGER
)
""")
connection.commit()


class User:
    def __init__(self, name, surname, email):
        self.name = name
        self.surname = surname
        self.email = email


users = [
    User("Emilia", "Gasimzada", "emiliagasimzada@gmail.com"),
    User("Asif", "Rzayev", "asifrzayev@gmail.com"),
    User("Charlie", "Brown", "charlie.brown@example.com")
]

class Book:
    def __init__(self, title, author, year_published, copies):
        self.title = title
        self.author = author
        self.year_published = year_published
        self.copies = copies
        self.log = []  

    def save_to_db(self):
        cur.execute("INSERT INTO books (title, author, year_published, copies) VALUES (?, ?, ?, ?)",
                    (self.title, self.author, self.year_published, self.copies))
        connection.commit()

    def borrow(self):
        if self.copies > 0:
            self.copies -= 1
            action = f"'{self.title}' borrowed."
            self.log_action(action)
            print(f"Book '{self.title}' is borrowed. Copies available now: {self.copies}")
        else:
            print(f"Sorry, no copies of '{self.title}' are available to borrow.")

    def return_book(self):
        self.copies += 1
        action = f"'{self.title}' returned."
        self.log_action(action)
        print(f"Book '{self.title}' is returned. Copies available now: {self.copies}")

    def log_action(self, action):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log.append(f"{timestamp}: {action}")

    def display_log(self):
        print("\nAction Log:")
        if not self.log:
            print("No actions recorded.")
        for entry in self.log:
            print(entry)

# Function to print available books
def print_available_books():
    cur.execute("SELECT title, author, year_published, copies FROM books WHERE copies > 0")
    available_books = cur.fetchall()
    
    print("\nAvailable Books:")
    for row in available_books:
        print(f"Title: {row[0]}, Author: {row[1]}, Year Published: {row[2]}, Copies Available: {row[3]}")

# Function to add a new book
def add_new_book():
    title = input("Enter the book title: ")
    author = input("Enter the author's name: ")
    year_published = int(input("Enter the year published: "))
    copies = int(input("Enter the number of copies available: "))
    
    new_book = Book(title, author, year_published, copies)
    new_book.save_to_db()
    print(f"Book '{title}' added to the database.")

# Function to get a book by title
def get_book_by_title(title):
    cur.execute("SELECT * FROM books WHERE title = ?", (title,))
    row = cur.fetchone()
    if row:
        return Book(row[1], row[2], row[3], row[4])
    return None

# User registration and login process
def user_login():
    name = input("Enter your name: ")
    surname = input("Enter your surname: ")
    email = input("Enter your email: ")

    # Check if the user matches any predefined users
    for user in users:
        if user.name == name and user.surname == surname and user.email == email:
            print("Verification confirmed. You are logged in!")
            return user  # Return the logged-in user

    print("Log in has failed.")
    return None

def user_sign_in():
    name = input("Create your name: ")
    surname = input("Create your surname: ")
    email = input("Create your email: ")

    # Create a new user and add to the users list
    new_user = User(name, surname, email)
    users.append(new_user)
    print("You have signed in successfully!")

# Main program
print("Welcome to the Library System!")

while True:
    action = input("\nType 'sign in' to create a new user or 'login' to log in: ").lower()

    if action == 'sign in':
        user_sign_in()
    elif action == 'login':
        logged_in_user = user_login()
        if logged_in_user:
            break  # Exit the login loop after successful login
    else:
        print("Invalid action. Please type 'sign in' or 'login'.")

# After successful login
while True:
    print("\nOptions:")
    print("1. View available books")
    print("2. Add a new book")
    print("3. Choose a book to borrow/return/check log")
    print("4. Exit")
    
    choice = input("Choose an option (1-4): ")
    
    if choice == '1':
        print_available_books()
    elif choice == '2':
        add_new_book()
    elif choice == '3':
        print_available_books()
        book_title = input("Enter the title of the book you want to interact with: ")
        selected_book = get_book_by_title(book_title)

        if selected_book:
            while True:
                action = input("Type 'borrow' to borrow the book, 'return' to return the book, or 'check log' to see the action log or 'exit' to quit: ").lower()
                
                if action == "borrow":
                    selected_book.borrow()
                elif action == "return":
                    selected_book.return_book()
                elif action == "check log":
                    selected_book.display_log()
                elif action == "exit":
                    break
                else:
                    print("Invalid input. Please type 'borrow', 'return', 'check log', or 'exit'.")
        else:
            print("Book not found. Please ensure the title is correct.")
    elif choice == '4':
        break
    else:
        print("Invalid choice. Please try again.")

# Close the connection
connection.close()