
import json
import os

FILE_NAME = "books.json"


class Book:
    def __init__(self, book_id, title, author,
                 issued=False, issued_to=""):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.issued = issued
        self.issued_to = issued_to


class Library:
    def __init__(self):
        self.books = {}
        self.load_books()

    def load_books(self):
        if os.path.exists(FILE_NAME):
            try:
                with open(FILE_NAME, "r") as file:
                    data = json.load(file)

                for item in data:
                    book = Book(
                        item["id"], item["title"], item["author"],
                        item["issued"], item["issued_to"]
                    )
                    self.books[book.book_id] = book
            except (json.JSONDecodeError, KeyError, TypeError):
                print("Could not read books.json.")

    def save_books(self):
        data = []

        for b in self.books.values():
            data.append({
                "id": b.book_id,
                "title": b.title,
                "author": b.author,
                "issued": b.issued,
                "issued_to": b.issued_to
            })

        with open(FILE_NAME, "w") as file:
            json.dump(data, file, indent=4)

    def add_book(self):
        bid = input("Enter book ID: ").strip()

        if not bid or bid in self.books:
            print("Invalid or duplicate book ID!")
            return

        title = input("Enter book title: ").strip()
        author = input("Enter author: ").strip()

        if not title or not author:
            print("Title and author cannot be empty.")
            return

        self.books[bid] = Book(bid, title, author)
        self.save_books()
        print("Book added successfully!")

    def search_book(self):
        keyword = input("Enter title or author: ").strip().lower()
        found = False

        for b in self.books.values():
            if keyword in b.title.lower() or keyword in b.author.lower():
                status = "Issued" if b.issued else "Available"
                print(
                    f"{b.book_id} | {b.title} | {b.author} | {status}"
                )
                found = True

        if not found:
            print("No matching books found.")

    def list_books(self):
        if not self.books:
            print("No books found.")
            return

        for b in self.books.values():
            status = "Issued" if b.issued else "Available"
            print(f"{b.book_id} | {b.title} | {b.author} | {status}")

    def issue_book(self):
        bid = input("Enter book ID: ").strip()

        if bid not in self.books:
            print("Book not found!")
            return

        book = self.books[bid]

        if book.issued:
            print("Book is already issued!")
            return

        person = input("Enter borrower's name: ").strip()
        if not person:
            print("Borrower's name cannot be empty.")
            return

        book.issued = True
        book.issued_to = person
        self.save_books()
        print("Book issued successfully!")

    def return_book(self):
        bid = input("Enter book ID: ").strip()

        if bid not in self.books:
            print("Book not found!")
        elif not self.books[bid].issued:
            print("This book is not issued.")
        else:
            self.books[bid].issued = False
            self.books[bid].issued_to = ""
            self.save_books()
            print("Book returned successfully!")

    def report(self):
        total = len(self.books)
        issued = sum(b.issued for b in self.books.values())

        print("Total books:", total)
        print("Issued books:", issued)
        print("Available books:", total - issued)


def main():
    library = Library()

    while True:
        print("\n--- Library Book Inventory Manager ---")
        print("1. Add book")
        print("2. Search book")
        print("3. List books")
        print("4. Issue book")
        print("5. Return book")
        print("6. Reports")
        print("7. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            library.add_book()
        elif choice == "2":
            library.search_book()
        elif choice == "3":
            library.list_books()
        elif choice == "4":
            library.issue_book()
        elif choice == "5":
            library.return_book()
        elif choice == "6":
            library.report()
        elif choice == "7":
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
