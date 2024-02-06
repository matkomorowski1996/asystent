class ExternalMemory:
    contacts = {}

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
    ExternalMemory.contacts[name] = phone
    return "Contact added successfully."

@input_error
def change_phone(name, new_phone):
    ExternalMemory.contacts[name] = new_phone
    return "Phone number updated successfully."

@input_error
def get_phone(name):
    return f"The phone number for {name} is {ExternalMemory.contacts[name]}."

def show_all():
    if not ExternalMemory.contacts:
        return "No contacts found."
    contacts_info = "\n".join([f"{name}: {phone}" for name, phone in ExternalMemory.contacts.items()])
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
            _, name, new_phone = command.split()
            print(change_phone(name, new_phone))
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
