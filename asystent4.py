import pickle
from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value=None):
        self._value = value

    def __str__(self):
        return str(self._value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

class Name(Field):
    pass

class Phone(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if not new_value.isdigit():
            raise ValueError("Phone number must contain only digits.")
        self._value = new_value

class Birthday(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        try:
            datetime.strptime(new_value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Please use YYYY-MM-DD.")
        self._value = new_value

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.birthday = Birthday(birthday) if birthday else None
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if str(p) != phone]

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if str(p) == old_phone:
                p.value = new_phone

    def days_to_birthday(self):
        if not self.birthday:
            return None
        today = datetime.now()
        next_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day)
        if next_birthday < today:
            next_birthday = datetime(today.year +  1, self.birthday.value.month, self.birthday.value.day)
        return (next_birthday - today).days

class AddressBook(UserDict):
    def __iter__(self):
        return iter(self.data.values())

    def __next__(self):
        pass

    def paginate(self, page_size):
        records = list(self.data.values())
        num_pages = (len(records) + page_size -  1) // page_size
        for page_num in range(num_pages):
            start_index = page_num * page_size
            end_index = min(start_index + page_size, len(records))
            yield records[start_index:end_index]

    def search_contacts(self, search_term):
        matching_contacts = []
        for name, record in self.data.items():
            if search_term in name or any(search_term in str(phone) for phone in record.phones):
                matching_contacts.append((name, record.phones))
        return matching_contacts

class ExternalMemory:
    contacts = AddressBook()

    @staticmethod
    def save_to_disk(filename='addressbook.dat'):
        with open(filename, 'wb') as f:
            pickle.dump(ExternalMemory.contacts, f)

    @staticmethod
    def load_from_disk(filename='addressbook.dat'):
        try:
            with open(filename, 'rb') as f:
                ExternalMemory.contacts = pickle.load(f)
        except FileNotFoundError:
            print("No saved address book found.")

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Error: Contact not found."
        except ValueError as e:
            return f"Error: {str(e)}"
        except IndexError:
            return "Error: Insufficient input."
    return inner

@input_error
def add_contact(name, phone, birthday=None):
    if name not in ExternalMemory.contacts:
        record = Record(name, birthday)
        record.add_phone(phone)
        ExternalMemory.contacts.add_record(record)
        return "Contact added successfully."
    else:
        return "Error: Contact already exists."

@input_error
def change_phone(name, old_phone, new_phone):
    if name in ExternalMemory.contacts:
        record = ExternalMemory.contacts[name]
        record.edit_phone(old_phone, new_phone)
        return "Phone number updated successfully."
    else:
        return "Error: Contact not found."

@input_error
def get_phone(name):
    if name in ExternalMemory.contacts:
        record = ExternalMemory.contacts[name]
        phones = ", ".join(str(phone) for phone in record.phones)
        return f"The phone number(s) for {name} is/are: {phones}."
    else:
        return "Error: Contact not found."

def show_all(page_size=10, page=1):
    if not ExternalMemory.contacts:
        return "No contacts found."
    paginated_records = ExternalMemory.contacts.paginate(page_size)
    page_num =  1
    for page_records in paginated_records:
        if page == page_num:
            contacts_info = "\n".join([f"{record.name}: {', '.join(str(phone) for phone in record.phones)}" for record in page_records])
            return contacts_info
        page_num +=  1
    return "Error: Page not found."

def search_contacts(search_term):
    results = ExternalMemory.contacts.search_contacts(search_term)
    for name, phones in results:
        print(f"{name}: {', '.join(str(phone) for phone in phones)}")

def main():
    ExternalMemory.load_from_disk()  # Załadowanie książki adresowej z dysku na początku
    print("How can I help you?")
    while True:
        command = input("Enter a command: ").lower()
        if '.' in command:
            ExternalMemory.save_to_disk()  # Zapianbie książki adresowej na dysku przed wyjściem
            print("Good bye!")
            break
        if command == "hello":
            print("How can I help you?")
        elif command.startswith("add"):
            _, name, phone, *birthday = command.split()
            birthday = birthday[0] if birthday else None
            print(add_contact(name, phone, birthday))
        elif command.startswith("change"):
            _, name, old_phone, new_phone = command.split()
            print(change_phone(name, old_phone, new_phone))
        elif command.startswith("phone"):
            _, name = command.split()
            print(get_phone(name))
        elif command.startswith("show all"):
            _, *args = command.split()
            page_size = int(args[0]) if args else  10
            page_num = int(args[1]) if len(args) >  1 else  1
            print(show_all(page_size, page_num))
        elif command.startswith("search"):
            _, search_term = command.split()
            search_contacts(search_term)
        elif command in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        else:
            print("Error: Command not recognized.")

if __name__ == "__main__":
    main()
