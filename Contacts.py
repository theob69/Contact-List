import csv
import os
import re

# Path to the CSV file
CSV_FILE = "contacts.csv"

# Function to validate an email
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Function to validate a phone number (simple format: 10 digits or XXX-XXX-XXXX)
def validate_phone(phone):
    pattern = r'^(\d{10}|\d{3}-\d{3}-\d{4})$'
    return re.match(pattern, phone) is not None

# Initialize the CSV file if it doesn't exist
def initialize_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Email", "Phone"])

# Read all contacts
def read_contacts():
    contacts = []
    try:
        with open(CSV_FILE, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                contacts.append(row)
    except FileNotFoundError:
        initialize_csv()
    return contacts

# Write a contact to the CSV
def write_contact(contact):
    with open(CSV_FILE, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["Name", "Email", "Phone"])
        writer.writerow(contact)

# Update all contacts (rewrite the file)
def update_contacts(contacts):
    with open(CSV_FILE, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["Name", "Email", "Phone"])
        writer.writeheader()
        writer.writerows(contacts)

# Add a contact
def add_contact():
    while True:
        name = input("Enter name: ").strip()
        if not name:
            print("Error: Name cannot be empty.")
            continue
        
        email = input("Enter email: ").strip()
        if not validate_email(email):
            print("Error: Invalid email.")
            continue
        
        phone = input("Enter phone (10 digits or XXX-XXX-XXXX): ").strip()
        if not validate_phone(phone):
            print("Error: Invalid phone number.")
            continue
        
        contact = {"Name": name, "Email": email, "Phone": phone}
        write_contact(contact)
        print("Contact added successfully!")
        break

# Display all contacts
def display_contacts():
    contacts = read_contacts()
    if not contacts:
        print("No contacts found.")
        return
    
    print("\nContact List:")
    for i, contact in enumerate(contacts, 1):
        print(f"{i}. Name: {contact['Name']}, Email: {contact['Email']}, Phone: {contact['Phone']}")

# Delete a contact
def delete_contact():
    contacts = read_contacts()
    if not contacts:
        print("No contacts to delete.")
        return
    
    display_contacts()
    try:
        index = int(input("Enter the contact number to delete: ")) - 1
        if 0 <= index < len(contacts):
            contacts.pop(index)
            update_contacts(contacts)
            print("Contact deleted successfully!")
        else:
            print("Error: Invalid contact number.")
    except ValueError:
        print("Error: Please enter a valid number.")

# Edit a contact
def edit_contact():
    contacts = read_contacts()
    if not contacts:
        print("No contacts to edit.")
        return
    
    display_contacts()
    try:
        index = int(input("Enter the contact number to edit: ")) - 1
        if 0 <= index < len(contacts):
            while True:
                name = input("Enter new name: ").strip()
                if not name:
                    print("Error: Name cannot be empty.")
                    continue
                
                email = input("Enter new email: ").strip()
                if not validate_email(email):
                    print("Error: Invalid email.")
                    continue
                
                phone = input("Enter new phone (10 digits or XXX-XXX-XXXX): ").strip()
                if not validate_phone(phone):
                    print("Error: Invalid phone number.")
                    continue
                
                contacts[index] = {"Name": name, "Email": email, "Phone": phone}
                update_contacts(contacts)
                print("Contact updated successfully!")
                break
        else:
            print("Error: Invalid contact number.")
    except ValueError:
        print("Error: Please enter a valid number.")

# Main menu
def menu():
    initialize_csv()
    while True:
        print("\n=== Contact Manager ===")
        print("1. Display contacts")
        print("2. Add a contact")
        print("3. Edit a contact")
        print("4. Delete a contact")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == "1":
            display_contacts()
        elif choice == "2":
            add_contact()
        elif choice == "3":
            edit_contact()
        elif choice == "4":
            delete_contact()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Error: Invalid choice. Please enter a number between 1 and 5.")

# Run the application
if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\nProgram interrupted. Goodbye!")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")