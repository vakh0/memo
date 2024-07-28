import sys
from diarybook import Diary, DiaryBook
from util import read_from_json_into_application, read_users_from_json, write_users_to_json, write_diaries_to_json

class Menu:

    def __init__(self):
        self.diarybook = DiaryBook()
        self.current_user = None
        self.users = read_users_from_json('users.json')

        self.choices = {
            "1": self.show_diaries,
            "2": self.add_diary,
            "3": self.search_diaries,
            "4": self.sort_diaries_by_id,
            "5": self.sort_diaries_by_memo,
            "6": self.populate_database,
            "7": self.quit
        }

    def load_diaries(self):
        if self.current_user:
            self.diarybook.diaries = read_from_json_into_application('data.json', self.current_user)
        else:
            self.diarybook.diaries = []

    def display_menu(self):
        print(""" 
                     Notebook Menu  
                    1. Show diaries
                    2. Add diary
                    3. Search diaries
                    4. Sort diaries by ID
                    5. Sort diaries by memo
                    6. Populate database
                    7. Quit program
                    """)

    def run(self):
        print("Welcome to DiaryBook!")
        self.authenticate_user()
        self.load_diaries()

        while True:
            self.display_menu()
            choice = input("Enter an option: ")
            action = self.choices.get(choice)
            if action:
                action()
            else:
                print("{0} is not a valid choice".format(choice))

    def authenticate_user(self):
        while True:
            print("1. Register")
            print("2. Login")
            choice = input("Enter an option: ")
            if choice == "1":
                self.register()
            elif choice == "2":
                if self.login():
                    break
            else:
                print("{0} is not a valid choice".format(choice))

    def register(self):
        username = input("Enter a username: ")
        password = input("Enter a password: ")
        for user in self.users:
            if user['username'] == username:
                print("Username already exists!")
                return
        self.users.append({'username': username, 'password': password})
        write_users_to_json('users.json', self.users)
        print("Registration successful!")

    def login(self):
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        for user in self.users:
            if user['username'] == username and user['password'] == password:
                self.current_user = username
                print(f"Welcome, {username}!")
                return True
        print("Invalid username or password!")
        return False

    def show_diaries(self, diaries=None):
        if not diaries:
            diaries = self.diarybook.diaries
        for diary in diaries:
            print(f"{diary.id} - {diary.memo}")

    def add_diary(self):
        memo = input("Enter a memo: ")
        tags = input("Add tags: ")
        new_diary = self.diarybook.new_diary(memo, tags)
        write_diaries_to_json('data.json', self.current_user, self.diarybook.diaries)
        print("Your note has been added")

    def search_diaries(self):
        filter_text = input("Search for: ")
        diaries = self.diarybook.search_diary(filter_text)
        for diary in diaries:
            print(f"{diary.id} - {diary.memo}")

    def sort_diaries_by_id(self):
        self.diarybook.diaries.sort(key=lambda x: x.id)
        print("Diaries sorted by ID:")
        self.show_diaries()

    def sort_diaries_by_memo(self):
        self.diarybook.diaries.sort(key=lambda x: x.memo.lower())
        print("Diaries sorted by memo:")
        self.show_diaries()

    def populate_database(self):
        if self.current_user:
            diaries1 = read_from_json_into_application('data.json', self.current_user)
            for diary in diaries1:
                self.diarybook.diaries.append(diary)

    def quit(self):
        if self.current_user:
            write_diaries_to_json('data.json', self.current_user, self.diarybook.diaries)
        print("Thank you for using DiaryBook today")
        sys.exit(0)

if __name__ == "__main__":
    Menu().run()
