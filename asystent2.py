from collections import UserDict

class Field:
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    pass

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if str(p) != phone]

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if str(p) == old_phone:
                p.value = new_phone

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

class ExternalMemory:
    contacts = AddressBook()

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Error: Contact not found."
        except ValueError:
            return "Error: Invalid input."
        except IndexError:
            return "Error: Insufficient input."
    return inner

@input_error
def add_contact(name, phone):
    if name not in ExternalMemory.contacts:
        record = Record(name)
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

def show_all():
    if not ExternalMemory.contacts:
        return "No contacts found."
    contacts_info = "\n".join([f"{name}: {', '.join(str(phone) for phone in record.phones)}" for name, record in ExternalMemory.contacts.items()])
    return contacts_info

def main():
    print("How can I help you?")
    while True:
        command = input("Enter a command: ").lower()
        if '.' in command:
            print("Good bye!")
            break
        if command == "hello":
            print("How can I help you?")
        elif command.startswith("add"):
            _, name, phone = command.split()
            print(add_contact(name, phone))
        elif command.startswith("change"):
            _, name, old_phone, new_phone = command.split()
            print(change_phone(name, old_phone, new_phone))
        elif command.startswith("phone"):
            _, name = command.split()
            print(get_phone(name))
        elif command == "show all":
            print(show_all())
        elif command in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        else:
            print("Error: Command not recognized.")

if __name__ == "__main__":
    main()
